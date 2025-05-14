import re
from gemini import Explainer
from utility import get_user_mood, get_user_response, get_system_prompt
from pepperSocketSender import send_message_to_pepper
from google.genai import types


def generate_explainer_message(user, use_case, user_response):
    msg_parts = []

    if use_case != "base":
        msg_parts.append("Le caratteristiche dell'utente sono:")
        msg_parts.append(f"- Età: {user['age']}")
        msg_parts.append(f"- Sesso: {user['sex']}")
        msg_parts.append(f"- Tratto della personalità: {user['personality_traits']}")
        msg_parts.append(f"- Umore attuale: {user['current_mood']}")

    msg_parts.append(f"- Risposta dell'utente: {user_response}")

    return "\n".join(msg_parts)


def handle_conversation(explainer, user_response, user, use_case):
    # Crea il messaggio da inviare a Gemini
    message = generate_explainer_message(user, use_case, user_response)
    print(message)

    # Ottieni la risposta di Gemini
    response = explainer.ask_gemini(message)

    # Stampa la risposta
    print(response)

    # Invia la risposta di Gemini al robot
    send_message_to_pepper(response)


def hasUserGone(userResponse):
    if userResponse is None:
        return True

    # Usa regex per verificare "stop" come parola intera
    if re.search(r'\bstop\b', userResponse.lower()):
        return True

    return False


def main_free_speech(user, use_case):
    robot_folder = "prompt_pepper"
    use_case_file = "system_prompt_caso_base.txt" if use_case == "base" else "system_prompt_caso_avanzato.txt"
    initial_message = "^mode(contextual) Ciao! Hai qualcosa di cui vuoi parlarmi?"

    systemPrompt = get_system_prompt(f"./prompt/{robot_folder}/{use_case_file}")
    explainer = Explainer(systemPrompt)
    explainer.history.append(types.Content(parts=[types.Part(text=initial_message)], role='model'))

    input("OK, ora premi Invio quando vuoi proseguire...")

    if use_case != "base":
        user['current_mood'] = get_user_mood()

    # Pepper chiede all'utente se ha qualcosa di cui vuole parlare
    send_message_to_pepper(initial_message)

    userResponse = get_user_response()
    print("Risposta dell'utente:", userResponse)

    # Invia la risposta dell'utente a Gemini per ottenere una risposta
    handle_conversation(explainer, userResponse, user, use_case)

    userResponse = get_user_response()
    print("Risposta dell'utente:", userResponse)

    # Loop per la conversazione finché l'utente non termina
    while not hasUserGone(userResponse):
        if use_case != "base":
            user['current_mood'] = get_user_mood()
        handle_conversation(explainer, userResponse, user, use_case)

        userResponse = get_user_response()
        print("Risposta dell'utente:", userResponse)

    # Conclusione della conversazione
    message = "^mode(contextual) Va bene! ^start(animations/Stand/Emotions/Positive/Happy_2) " \
              "Spero che avremo l'occasione di riparlarci, a presto! ^wait(animations/Stand/Emotions/Positive/Happy_2)"
    send_message_to_pepper(message)
