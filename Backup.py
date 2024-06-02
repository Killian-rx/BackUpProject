import subprocess
import tkinter as tk
from tkinter import BOTTOM, messagebox, ttk
from datetime import datetime, timedelta
import threading
import time
import customtkinter

# Chemins de fichiers
LOCAL_DIR = "C:/Users/killi/OneDrive - Ynov/YNOV/Cours/Projet Infra/BackUpProject"
REMOTE_DIR = "/home/backupuser/backups/"

# Messages
BACKUP_SUCCESS_MSG = "La sauvegarde a été effectuée avec succès."
RETRIEVE_SUCCESS_MSG = "Les fichiers ont été récupérés avec succès."
ERROR_MSG = "Une erreur s'est produite."

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")


def run_backup(direction):
    if direction == "backup":
        cmd = [
            "scp", "-r", f"{LOCAL_DIR}/sauvegarde",
            f"backupuser@192.168.159.131:{REMOTE_DIR}"
        ]
        message_title = "Backup Successful"
        message_text = BACKUP_SUCCESS_MSG
    elif direction == "retrieve":
        cmd = [
            "scp", "-r", f"backupuser@192.168.159.131:{REMOTE_DIR}/sauvegarde",
            f"{LOCAL_DIR}"
        ]
        message_title = "Retrieve Successful"
        message_text = RETRIEVE_SUCCESS_MSG

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        messagebox.showinfo(message_title, message_text)
    else:
        messagebox.showerror("Error", ERROR_MSG)


def schedule_backup():
    time_str = time_entry.get()
    frequency = frequency_combobox.get()
    try:
        schedule_time = datetime.strptime(time_str, '%H:%M').time()
        now = datetime.now().time()
        first_run = datetime.combine(datetime.today(), schedule_time).time()
        if first_run < now:
            first_run = (datetime.combine(datetime.today() + timedelta(days=1),
                                          schedule_time)).time()

        if frequency == "Quotidienne":
            interval = 24 * 60 * 60
        elif frequency == "Tous les deux jours":
            interval = 2 * 24 * 60 * 60
        elif frequency == "Vendredi":
            days_until_friday = (4 - datetime.today().weekday() + 7) % 7
            interval = days_until_friday * 24 * 60 * 60

        threading.Thread(target=schedule_task,
                         args=(first_run, interval)).start()
        messagebox.showinfo(
            "Scheduled", f"Backup scheduled {frequency.lower()} at {time_str}")

    except ValueError:
        messagebox.showerror("Error", "Invalid time format")


def schedule_task(first_run, interval):
    while True:
        now = datetime.now().time()
        if now >= first_run:
            run_backup("backup")
            first_run = (datetime.combine(
                datetime.today() + timedelta(seconds=interval),
                first_run)).time()
        time.sleep(60)


# Création de l'interface utilisateur
root = customtkinter.CTk()

root.title("Backup Interface")
root.geometry("500x350")

# Appliquer les styles depuis le fichier styles.py


# Fonction pour centrer la fenêtre au centre de l'écran
def center_window(window):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    window.geometry('+{}+{}'.format(x, y))


center_window(root)


# Fonction appelée lorsque le bouton de sauvegarde est cliqué
def on_backup_click():
    run_backup("backup")


# Fonction appelée lorsque le bouton de récupération est cliqué
def on_retrieve_click():
    run_backup("retrieve")


titre = customtkinter.CTkLabel(master=root,
                               text="Backup Infrastructure SI",
                               font=("Helvetica", 20),
                               pady=15)
titre.pack(pady=5)

# Création du cadre gauche
left_frame = customtkinter.CTkFrame(root)
left_frame.pack(side="left", fill="y")
left_frame.place(relx=0.25, rely=0.4, anchor="center")
left_frame.pack_propagate(False)

# Création du cadre droit
right_frame = customtkinter.CTkFrame(root)
right_frame.pack(side="right", fill="both", expand=True)
right_frame.place(relx=0.75, rely=0.5, anchor="center")
right_frame.pack_propagate(False)

# Création du bouton de sauvegarde
backup_button = customtkinter.CTkButton(master=left_frame,
                                        text="Faire une Backup",
                                        command=on_backup_click)
backup_button.grid(row=0, column=0, padx=10, pady=10)

# Création du bouton de récupération
retrieve_button = customtkinter.CTkButton(
    master=left_frame,
    text="Restaurer les fichiers",
    command=on_retrieve_click,
)
retrieve_button.grid(row=1, column=0, padx=10, pady=10)

# Entrée pour l'heure de sauvegarde
time_label = customtkinter.CTkLabel(master=right_frame,
                                    text="Démarré à (HH:MM):")
time_label.pack(pady=5)

time_entry = customtkinter.CTkEntry(master=right_frame)
time_entry.pack(pady=5)

# Liste déroulante pour choisir la fréquence de la sauvegarde
frequency_label = customtkinter.CTkLabel(master=right_frame,
                                         text="Fréquence de la Backup:")
frequency_label.pack(pady=5)

frequency_options = ["Quotidienne", "Tous les deux jours", "Vendredi"]
frequency_combobox = customtkinter.CTkComboBox(master=right_frame,
                                               values=frequency_options,
                                               state="readonly",
                                               corner_radius=10,
                                               dropdown_hover_color=("grey"),
                                               hover=True)
frequency_combobox.set("Quotidienne")
frequency_combobox.pack(pady=5)


def change_appearance_mode(new_mode):
    customtkinter.set_appearance_mode(new_mode)

# Combobox pour light dark system
mode_options = ["System", "Light", "Dark"]
mode_combobox = customtkinter.CTkComboBox(master=root,
                                               values=mode_options,
                                               state="readonly",
                                               command=change_appearance_mode,
                                               corner_radius=10,
                                               dropdown_hover_color=("grey"),
                                               
                                               hover=True)
mode_combobox.set("Dark")
mode_combobox.place(x=55, y=238)

# Création du bouton de programmation de sauvegarde
schedule_button = customtkinter.CTkButton(master=right_frame,
                                          text="Plannifier une Backup",
                                          command=schedule_backup)
schedule_button.pack(pady=10)

titre2 = customtkinter.CTkLabel(
    master=root,
    text="Arthur Chessé & Kilian Roux",
    font=("Helvetica", 10),
)
titre2.pack(side="bottom", pady=5)

# Lancement de la boucle principale de l'interface utilisateur
root.mainloop()
