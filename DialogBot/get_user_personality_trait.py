import tkinter as tk
from tkinter import ttk
import random


def get_personality_data():
    user_data = {
        "trait_scores": {
            "Extrovert": 0,
            "Agreeable": 0,
            "Conscientious": 0,
            "Nevrotic": 0,
            "Open": 0
        },
        "question_scores": []
    }

    def submit():
        scores = {
            "Extrovert": sum([6 - responses[i].get() if i == 0 else responses[i].get() for i in [0, 5]]),
            "Agreeable": sum([6 - responses[i].get() if i == 1 else responses[i].get() for i in [1, 6]]),
            "Conscientious": sum([6 - responses[i].get() if i == 2 else responses[i].get() for i in [2, 7]]),
            "Nevrotic": sum([6 - responses[i].get() if i == 3 else responses[i].get() for i in [3, 8]]),
            "Open": sum([6 - responses[i].get() if i == 4 else responses[i].get() for i in [4, 9]]),
        }

        # Add the total scores for each trait
        user_data["trait_scores"].update(scores)

        # Collect individual question scores
        user_data["question_scores"] = [response.get() for response in responses]

        root.destroy()

    root = tk.Tk()
    root.title("Questionario Personalità Big Five")
    root.attributes('-fullscreen', True)

    # Uscire dalla modalità fullscreen premendo ESC
    root.bind("<Escape>", lambda event: root.attributes('-fullscreen', False))

    main_frame = ttk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(main_frame)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)

    scrollable_frame = ttk.Frame(canvas)
    scrollable_frame_id = canvas.create_window((root.winfo_screenwidth() // 2, 0),
                                               window=scrollable_frame, anchor="n")

    def update_scroll_region(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(scrollable_frame_id, width=canvas.winfo_width() - 50)

    scrollable_frame.bind("<Configure>", update_scroll_region)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(0, weight=1)

    def on_mouse_wheel(event):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)
    canvas.bind_all("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))

    tk.Label(scrollable_frame, text="Quanto bene le seguenti affermazioni descrivono la tua personalità?",
             font=("Arial", 20, "bold")).pack(pady=10)
    tk.Label(scrollable_frame, text="1: Fortemente in disaccordo     5: Fortemente d'accordo",
             font=("Arial", 13, "italic")).pack(pady=10)

    statements = [
        "è riservato", "è generalmente fiducioso", "tende a essere pigro",
        "è rilassato, gestisce bene lo stress", "ha pochi interessi artistici",
        "è estroverso, socievole", "tende a trovare difetti negli altri",
        "svolge un lavoro accurato", "si innervosisce facilmente", "ha un'immaginazione vivace"
    ]

    responses = []
    for idx, statement in enumerate(statements):
        tk.Label(scrollable_frame, text=f"Mi vedo come qualcuno che {statement}",
                 font=("Arial", 14, "normal")).pack(pady=5)
        response_var = tk.IntVar(value=3)
        response_scale = tk.Scale(scrollable_frame, from_=1, to=5, orient="horizontal",
                                  variable=response_var, font=("Arial", 14), tickinterval=1)
        response_scale.config(length=250)
        response_scale.pack(pady=(0, 20))
        responses.append(response_var)

    submit_button = tk.Button(
        scrollable_frame, text="Invia", command=submit,
        font=("Arial", 14, "bold"), padx=20, pady=1,
        bg="#004080", fg="white", bd=5
    )

    submit_button.pack(pady=50)

    root.mainloop()
    return user_data


def determine_personality_trait(user_data):
    scores = user_data["trait_scores"]
    max_score = max(scores.values())
    top_traits = [trait for trait, score in scores.items() if score == max_score]
    return random.choice(top_traits)


def get_user_pers_trait():
    pers_traits = get_personality_data()
    print("Tratti di personalità:", pers_traits)
    return determine_personality_trait(pers_traits)


if __name__ == "__main__":
    personality_traits = get_personality_data()
    print("Tratti di personalità:", personality_traits)
    most_probable_trait = determine_personality_trait(personality_traits)
    print("Il tratto di personalità più probabile è:", most_probable_trait)
