import re
import cv2
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import base64
import json


class Explainer:
    def __init__(self, system_prompt):
        load_dotenv("properties.env")
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.system_prompt = system_prompt
        self.history = []

    def ask_gemini(self, message):
        self.history.append(types.Content(parts=[types.Part(text=message)], role='user'))
        contents = self.history

        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
            ),
        )

        raw_reply = response.text
        self.history.append(types.Content(parts=[types.Part(text=raw_reply)], role='model'))
        return raw_reply

    def ask_gemini_without_history(self, message, model='gemini-1.5-flash'):
        response = self.client.models.generate_content(
            model=model,
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
            ),
        )

        return response.text

    # https://ai.google.dev/gemini-api/docs/vision?lang=python
    def analyze_emotion(self, image):
        """Analizza le emozioni in un'immagine e restituisce il livello di stress e l'etichetta dell'emozione."""

        try:
            # Converti l'immagine da NumPy array a JPEG binario
            _, buffer = cv2.imencode(".jpg", image)
            image_base64 = base64.b64encode(buffer).decode("utf-8")

            prompt = (
                "Analizza l'immagine e restituisci un JSON con i seguenti campi: "
                "'stress_level' (float tra 0 e 1) e 'emotion' (stringa con etichetta tra "
                "'happy', 'sad', 'angry', 'fear', 'neutral'). "
                "Rispondi solo con JSON."
            )

            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[
                    types.Content(
                        parts=[
                            types.Part(text=prompt),
                            types.Part(inline_data=types.Blob(mime_type="image/jpeg", data=image_base64))
                        ],
                        role='user'
                    )
                ]
            )

            raw_text = response.text.strip()

            # Rimuove eventuali blocchi di codice markdown come ```json ... ```
            cleaned_text = re.sub(r"```json|```", "", raw_text).strip()

            # Tenta di decodificare il JSON
            return json.loads(cleaned_text)

        except (json.JSONDecodeError, AttributeError, KeyError, TypeError, Exception):
            return {"emotion": "unknown", "stress_level": 0.0, "error": "Invalid or missing data"}


'''
Esempio d'uso di Gemini come Mood Detector

def take_picture():
    cap = cv2.VideoCapture(0)  # Apri la webcam
    ret, frame = cap.read()  # Cattura un frame
    cap.release()  # Rilascia la webcam
    return frame if ret else None


explainer = Explainer('')
image = take_picture()
response = explainer.analyze_emotion(image)
print(response)
print(response['emotion'])
'''

'''
# Esempio di utilizzo
system_prompt = "Sei un utile assistente che risponde a domande."
explainer = Explainer(system_prompt)

user_input1 = "Qual è la capitale della Francia?"
response1 = explainer.ask_gemini(user_input1)
print(f"Utente: {user_input1}")
print(f"Gemini: {response1}")

user_input2 = "E la popolazione?"
response2 = explainer.ask_gemini(user_input2)
print(f"Utente: {user_input2}")
print(f"Gemini: {response2}")

user_input3 = "qual è la prima domanda che ti ho fatto?"
response3 = explainer.ask_gemini(user_input3)
print(f"Utente: {user_input3}")
print(f"Gemini: {response3}")
'''