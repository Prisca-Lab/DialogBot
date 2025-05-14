import random
import time
from getUserFromGUI import get_user_data
from get_user_personality_trait import get_personality_data, determine_personality_trait
from free_speech import main_free_speech


def fetch_user():
    user_info = get_user_data()
    user = {'age': user_info['Età'], 'sex': user_info['Sesso']}

    return user


def get_use_case():
    scelta = input("Vuoi scegliere manualmente la condizione? (sì/no): ").strip().lower()

    tipologie = ["base", "advanced"]
    descrizioni = {
        "base": "Caso base - Free Speech",
        "advanced": "Caso avanzato - Free Speech"
    }

    if scelta in ["sì", "si", "s"]:
        while True:
            tipo_input = input("Scegli la modalità (base [b] / advanced [a]): ").strip().lower()
            if tipo_input in ["base", "b"]:
                tipo = "base"
                break
            elif tipo_input in ["advanced", "a"]:
                tipo = "advanced"
                break
            else:
                print("Modalità non valida. Riprova (usa 'base', 'b', 'advanced' o 'a').")
    else:
        tipo = random.choice(tipologie)

    descrizione = descrizioni[tipo]
    print(f"\nCondizione scelta: {descrizione}")
    time.sleep(1.5)
    return descrizione


def rewriteUseCase(wrapped_string):
    """
    Converte la stringa descrittiva in 'base' o 'advanced'
    """
    if "avanzato" in wrapped_string.lower():
        return "advanced"
    else:
        return "base"


def main():
    use_case_wrapped = get_use_case()
    use_case = rewriteUseCase(use_case_wrapped)

    user = fetch_user()

    personality_data = get_personality_data()
    user['personality_traits'] = determine_personality_trait(personality_data)

    main_free_speech(user, use_case)


if __name__ == "__main__":
    main()
