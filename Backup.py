import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import threading
import time

# Chemins de fichiers
LOCAL_DIR = "C:/Users/killi/OneDrive - Ynov/YNOV/Cours/Projet Infra/BackUpProject"
REMOTE_DIR = "/home/backupuser/backups/"

# Messages
BACKUP_SUCCESS_MSG = "La sauvegarde a été effectuée avec succès."
RETRIEVE_SUCCESS_MSG = "Les fichiers ont été récupérés avec succès."
ERROR_MSG = "Une erreur s'est produite."

def run_backup(direction):
    if direction == "backup":
        cmd = ["scp", "-r", f"{LOCAL_DIR}/sauvegarde", f"backupuser@192.168.159.131:{REMOTE_DIR}"]
        message_title = "Backup Successful"
        message_text = BACKUP_SUCCESS_MSG
    elif direction == "retrieve":
        cmd = ["scp", "-r", f"backupuser@192.168.159.131:{REMOTE_DIR}/sauvegarde", f"{LOCAL_DIR}"]
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
            first_run = (datetime.combine(datetime.today() + timedelta(days=1), schedule_time)).time()

        if frequency == "Quotidienne":
            interval = 24 * 60 * 60
        elif frequency == "Tous les deux jours":
            interval = 2 * 24 * 60 * 60
        elif frequency == "Vendredi":
            days_until_friday = (4 - datetime.today().weekday() + 7) % 7
            interval = days_until_friday * 24 * 60 * 60

        threading.Thread(target=schedule_task, args=(first_run, interval)).start()
        messagebox.showinfo("Scheduled", f"Backup scheduled {frequency.lower()} at {time_str}")

    except ValueError:
        messagebox.showerror("Error", "Invalid time format")

def schedule_task(first_run, interval):
    while True:
        now = datetime.now().time()
        if now >= first_run:
            run_backup("backup")
            first_run = (datetime.combine(datetime.today() + timedelta(seconds=interval), first_run)).time()
        time.sleep(60)  

# Création de l'interface utilisateur
root = tk.Tk()
root.title("Backup Interface")
root.geometry("500x350")

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

# Création du bouton de sauvegarde
backup_button = tk.Button(
    root, 
    text="Faire une Backup", 
    command=on_backup_click,
    relief="raised",
    cursor="hand2",
)
backup_button.pack(pady=10)

# Ligne horizontale
separator1 = ttk.Separator(root, orient='horizontal')
separator1.pack(fill='x', pady=10, padx=150)

# Création du bouton de récupération
retrieve_button = tk.Button(
    root,
    text="Restaurer les fichiers",
    command=on_retrieve_click,
    relief="raised",
    cursor="hand2",
)
retrieve_button.pack(pady=10)

# Ligne horizontale
separator2 = ttk.Separator(root, orient='horizontal')
separator2.pack(fill='x', pady=10, padx=150)

# Entrée pour l'heure de sauvegarde
time_label = tk.Label(root, text="Démarré à (HH:MM):")
time_label.pack(pady=5)
time_entry = tk.Entry(root)
time_entry.pack(pady=5)

# Liste déroulante pour choisir la fréquence de la sauvegarde
frequency_label = tk.Label(root, text="Fréquence de la Backup:")
frequency_label.pack(pady=5)
frequency_options = ["Quotidienne", "Tous les deux jours", "Tous les Vendredi"]
frequency_combobox = ttk.Combobox(root, values=frequency_options, state="readonly")
frequency_combobox.set("Quotidienne")
frequency_combobox.pack(pady=5)

# Création du bouton de programmation de sauvegarde
schedule_button = tk.Button(
    root, 
    text="Plannifier une Backup", 
    command=schedule_backup,
    relief="raised",
    cursor="hand2",
)
schedule_button.pack(pady=10)

# Lancement de la boucle principale de l'interface utilisateur
root.mainloop()
