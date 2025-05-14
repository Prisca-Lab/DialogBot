from gemini import Explainer
from pepperSocketSender import pepper_get_image, pepper_fake_listening_feedback
import speech_recognition as sr


def get_user_mood():
    image = pepper_get_image()
    explainer = Explainer('')
    response = explainer.analyze_emotion(image)
    print(response)
    return response['emotion']


def configure_recognizer(secondi_pausa_per_stop=3):
    """Configura il riconoscitore e il microfono per la registrazione."""
    recognizer_ = sr.Recognizer()
    mic_ = sr.Microphone()

    with mic_ as source:
        recognizer_.adjust_for_ambient_noise(source, duration=1)  # Aumenta la calibrazione del rumore
        recognizer_.dynamic_energy_threshold = False
        recognizer_.energy_threshold = 400
        recognizer_.pause_threshold = float(secondi_pausa_per_stop)

    return recognizer_, mic_


# Utilizzo della funzione
recognizer, mic = configure_recognizer()


def get_transcribed_speech(secondi_pausa_per_stop=3):
    with mic as source:
        try:
            print("In ascolto...")
            audio_data = recognizer.listen(source)
            print(f"Ok, registrazione terminata (rilevata pausa di {recognizer.pause_threshold}s). "
                  f"Provo a trascrivere...")
        except sr.WaitTimeoutError:
            print(f"Nessun parlato rilevato entro il tempo limite iniziale ({secondi_pausa_per_stop}s).")
            return None
        except Exception as e:
            print(f"Errore durante la cattura dell'audio: {e}")
            return None

        # Se l'audio è stato catturato, prova a trascriverlo
        if audio_data:
            try:
                pepper_fake_listening_feedback(start=False)
                print("Invio audio per il riconoscimento a Google...")
                testo_trascritto = recognizer.recognize_google(audio_data, language='it-IT')
                print("Trascrizione ottenuta con successo.")
                return testo_trascritto
            except sr.UnknownValueError:
                print("Google Speech Recognition non è riuscito a capire l'audio.")
                return None
            except sr.RequestError as e:
                print(f"Errore nella richiesta a Google Speech Recognition; {e}")
                return None
            except Exception as e:
                print(f"Errore imprevisto durante il riconoscimento: {e}")
                return None
        else:
            # Se siamo qui senza audio_data, qualcosa è andato storto in listen()
            # anche se non ha sollevato eccezioni note.
            print("Nessun dato audio valido è stato registrato.")
            return None


def get_user_response():
    userResponse = None
    pepper_fake_listening_feedback(start=True)

    while userResponse is None:
        print("\nIl robot è in attesa di una tua risposta...")
        userResponse = get_transcribed_speech()
    return userResponse


def get_system_prompt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Errore nella lettura del file {file_path}: {e}")
        exit(1)
