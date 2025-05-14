import requests
import json


def send_message_to_furhat(msg, age):
    """
        Funzione per inviare un messaggio a Furhat affinché lo pronunci,
        includendo l'età dell'utente. In base all'età, sarà scelta una voce (di Acapela)
        infantile oppure adulta.
    """
    url = "http://localhost:8081/speak"
    headers = {"Content-Type": "application/json"}
    age = int(age)

    data = {
        "text": msg,
        "age": age
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code != 200:
        print("Errore nella richiesta:", response.status_code, response.text)


def furhat_recognize_speech():
    """
    Funzione per inviare una richiesta di riconoscimento vocale al server che gestisce Furhat.
    Restituisce il testo riconosciuto dal robot.
    """
    url = "http://localhost:8081/fetch_speech"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Errore: Stato HTTP {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Errore di connessione: {e}")
        return None


if __name__ == "__main__":
    message = input("Inserisci un messaggio per Furhat: ")
    send_message_to_furhat(message, 10)  # Esempio, con età di 10 anni
