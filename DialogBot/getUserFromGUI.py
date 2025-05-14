import tkinter as tk
from tkinter import ttk


def get_user_data():
    user_data = {}

    def validate_fields():
        fields_valid = age_var.get().isdigit() and gender_var.get() in ["Maschio", "Femmina", "Altro"]
        submit_button.config(state="normal" if fields_valid else "disabled")

    def submit():
        user_data.update({
            "Età": age_var.get(),
            "Sesso": gender_var.get(),
        })
        root.destroy()

    root = tk.Tk()
    root.title("Questionario Utente")
    root.attributes('-fullscreen', True)  # Modalità tutto schermo

    # Uscire dalla modalità fullscreen premendo ESC
    root.bind("<Escape>", lambda event: root.attributes('-fullscreen', False))

    # Porta la finestra in primo piano
    root.lift()
    root.attributes('-topmost', True)
    root.after(1000, lambda: root.attributes('-topmost', False))

    age_var = tk.StringVar()
    gender_var = tk.StringVar()

    # Titolo sopra il questionario
    title_label = tk.Label(root, text="Questionario Utente", font=("Arial", 24, "bold"))
    title_label.pack(pady=20)

    tk.Label(root, text="Età", font=("Arial", 16)).pack(pady=10)
    age_entry = tk.Entry(root, textvariable=age_var, font=("Arial", 14))
    age_entry.pack(pady=10)

    tk.Label(root, text="Sesso", font=("Arial", 16)).pack(pady=10)
    gender_combo = ttk.Combobox(root, textvariable=gender_var, values=["Maschio", "Femmina", "Altro"], state="readonly",
                                font=("Arial", 14))
    gender_combo.pack(pady=10)

    submit_button = tk.Button(
        root, text="Invia", command=submit, state="disabled",
        font=("Arial", 14, "bold"), padx=20, pady=1,
        bg="#004080", fg="white", bd=5
    )
    submit_button.pack(pady=20)

    age_var.trace_add("write", lambda *args: validate_fields())
    gender_var.trace_add("write", lambda *args: validate_fields())

    root.mainloop()
    return user_data


if __name__ == "__main__":
    user_info = get_user_data()
    print("Dati utente:", user_info)
