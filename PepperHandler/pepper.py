# coding=utf-8
import threading
import qi
import socket
from PeopleTracker import PeopleTracker
import struct


class Pepper:
    def __init__(self, ip, port):
        # Connessione al robot
        self.session = qi.Session()
        self.stopRotatingEyes = False
        try:
            # Real furhat IP: 143.225.85.X
            self.session.connect("tcp://" + ip + ":" + port)
        except RuntimeError:
            print("Impossibile connettersi al robot.")
            return

        self.tracker = PeopleTracker(self.session)
        self.alza_testa()
        self.wakeup()

    def alza_testa(self, angolo=-0.2, velocita=0.2):
        """
        Solleva la testa di Pepper impostando un angolo negativo su HeadPitch.
        Angolo in radianti: -0.5 (su) a +0.5 (giù). 0 è orizzontale.
        """
        try:
            motion_service = self.session.service("ALMotion")
            motion_service.setStiffnesses("Head", 1.0)  # Attiva i motori della testa
            motion_service.setAngles("HeadPitch", angolo, velocita)
        except Exception as e:
            print("Errore nel sollevare la testa:", e)

    def getImageFromCamera(self):
        video_service = self.session.service("ALVideoDevice")

        resolution = 2  # Controlla image_size per la risoluzione, max è 3. 2 è il valore raccomandato.
        colorSpace = 13  # BGR, for openCV

        # image_size = ['320x240x3', '640x480x3', '1280x960x3']

        videoClient = video_service.subscribe("get_image", resolution, colorSpace, 5)

        naoImage = video_service.getImageRemote(videoClient)
        w = naoImage[0]
        h = naoImage[1]
        img = naoImage[6]
        video_service.unsubscribe(videoClient)

        return w, h, img

    """
    The ALAnimatedSpeech module allows you to make the robot talk in an expressive way.
    http://doc.aldebaran.com/2-5/naoqi/audio/alanimatedspeech.html#alanimatedspeech
    
    List of Pepper animations:
    http://doc.aldebaran.com/2-5/naoqi/motion/alanimationplayer-advanced.html#animationplayer-list-behaviors-pepper
    """

    def runAnimatedSpeech(self, message):
        """
        Sends an animated speech message to the Pepper robot using the ALAnimatedSpeech service.

        The message can include special control sequences to manage animations:
          - `^mode(contextual)`: Enables contextual animations when keywords such as "I", "you", or "all" are detected.
          - `^mode(disabled)`: Disables automatic gestures, requiring explicit animation commands.
          - `^start(animation_path)`: Initiates a specific animation.
          - `^wait(animation_path)`: Waits for the specified animation to finish before continuing.

        Example message: "^mode(contextual) Hello! ^start(animations/Stand/Emotions/Positive/Happy_2) Nice to meet
        you ^wait(animations/Stand/Emotions/Positive/Happy_2) My name is Pepper"

        Parameters:
            message (str): The text of the message, including embedded animation commands.

        Returns:
            None

        In case of an error while creating the ALAnimatedSpeech proxy or sending the message,
        an error message will be printed.
        """
        try:
            animated_speech = self.session.service("ALAnimatedSpeech")
        except Exception as e:
            print("Error creating ALAnimatedSpeech proxy:", e)
            return

        try:
            print("Sending animated speech message:", message)
            animated_speech.say(message, blocking=True)
        except Exception as e:
            print("Error sending animated speech message:", e)

    def wakeup(self):
        try:
            motion_service = self.session.service("ALMotion")
            motion_service.wakeUp()
            print("Pepper si è svegliato.")
        except Exception as e:
            print("Errore nel wakeup di Pepper:", e)

    def fake_listening_feedback(self, start):
        """
        Simula il feedback di ascolto di Pepper senza attivare il riconoscimento vocale,
        riproducendo lo stesso suono che Pepper usa quando entra in modalità ascolto.
        """
        try:
            leds_service = self.session.service("ALLeds")
            audio_service = self.session.service("ALAudioPlayer")

            if start:
                # Riproduce il suono di sistema usato per il riconoscimento vocale
                audio_service.playFile("/opt/aldebaran/share/naoqi/wav/begin_reco.wav", 1.0, 0.0)

                # Funzione per ruotare gli occhi in un thread separato
                def rotate_eyes():
                    while not self.stopRotatingEyes:
                        print("Eseguo rotateEyes")
                        leds_service.rotateEyes(0x0000FF, 0.6,
                                                3)  # Blu, transizione in 0.6s, per un totale di 3 secondi

                # Esegui il movimento degli occhi in un thread separato
                self.stopRotatingEyes = False
                eye_thread = threading.Thread(target=rotate_eyes)
                eye_thread.start()

                # Il programma principale continua mentre gli occhi ruotano
                print("Pepper simula l'ascolto...")
            else:
                # Spegnere gli occhi
                self.stopRotatingEyes = True
                leds_service.fadeRGB("FaceLeds", 0xFFFFFF, 0.5)  # Torna al colore predefinito
                audio_service.playFile("/opt/aldebaran/share/naoqi/wav/end_reco.wav", 1.0, 0.0)
                print("Pepper ha finito di ascoltare.")

        except Exception as e:
            print("Errore nella simulazione dell'ascolto:", e)


def start_server(pepper_ip, pepper_port):
    host = '127.0.0.1'  # Indirizzo locale per la connessione
    port = 12345  # Porta su cui il server ascolta

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    # Imposta un timeout per evitare che accept() blocchi tutto
    server_socket.settimeout(1.0)

    pepper_client = Pepper(pepper_ip, pepper_port)

    print("Server in ascolto su {}:{}".format(host, port))
    tracking_Started = False

    try:
        while True:
            try:
                connection, address = server_socket.accept()
                print('Connessione stabilita con:', address)

                data = connection.recv(1024).decode('utf-8', errors='replace').strip()
                if not data or len(data) == 0:
                    connection.close()
                    continue
                if not tracking_Started:
                    tracking_Started = True
                    # Avvia il tracking
                    pepper_client.tracker.start_tracking()

                data = data.encode("utf-8", "replace")
                print("Ricevuto dal client:", data)

                if data.lower() == "get_image":
                    w, h, image = pepper_client.getImageFromCamera()
                    connection.sendall(struct.pack("ii", w, h))
                    connection.sendall(image)
                elif data.lower() == "fake_listening_feedback_start":
                    pepper_client.fake_listening_feedback(start=True)
                elif data.lower() == "fake_listening_feedback_stop":
                    pepper_client.fake_listening_feedback(start=False)
                else:
                    pepper_client.runAnimatedSpeech(data)
                    connection.sendall("ok".encode('utf-8'))

                connection.close()

            except socket.timeout:
                # Il timeout evita il blocco su accept(), permettendo di controllare Ctrl+C
                continue

    except KeyboardInterrupt:
        print("\nServer interrotto. Chiusura in corso...")

    finally:
        pepper_client.tracker.stop_tracking()
        server_socket.close()
        print("Server chiuso.")


if __name__ == "__main__":
    pepper_ip = '143.225.85.168'
    pepper_port = '9559'
    start_server(pepper_ip, pepper_port)
