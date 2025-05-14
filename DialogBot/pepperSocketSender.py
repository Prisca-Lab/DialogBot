import socket
import numpy as np
import cv2
import struct


def send_message_to_pepper(message):
    host = '127.0.0.1'  # Indirizzo del server
    port = 12345  # La stessa porta configurata nel server

    # Crea un socket per la connessione
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Invia il messaggio
    client_socket.send(message.encode('utf-8'))
    client_socket.recv(1024).decode('utf-8')
    client_socket.close()


def pepper_fake_listening_feedback(start=True):
    """
        Funzione per simulare i suoni di inizio e fine listen di Pepper.
    """
    host = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Invia la richiesta di riconoscimento vocale
    if start:
        client_socket.sendall("fake_listening_feedback_start".encode('utf-8'))
    else:
        client_socket.sendall("fake_listening_feedback_stop".encode('utf-8'))
    client_socket.close()


def pepper_get_image():
    """
        Funzione per inviare una richiesta di ottenere un'immagine al server che gestisce Pepper.
        Riceve i dati dell'immagine e li converte in un formato utilizzabile.
    """

    host = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Invia la richiesta per ottenere un'immagine
    client_socket.sendall("get_image".encode('utf-8'))

    # Riceve la dimensione dell'immagine (w e h sono due interi da 4 byte ciascuno)
    header = client_socket.recv(8)
    w, h = struct.unpack("ii", header)

    # Riceve i dati dell'immagine
    data = b""
    while True:
        packet = client_socket.recv(4096)
        if not packet:
            break
        data += packet

    client_socket.close()

    # Converti in un array numpy e ridimensionalo correttamente
    image_array = np.frombuffer(data, dtype=np.uint8).reshape((h, w, 3))

    # Converti in formato BGR per OpenCV
    image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

    if image is None:
        print("Errore nella decodifica dell'immagine")
        return None

    # window_name = 'image'
    # cv2.imshow(window_name, image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return image

