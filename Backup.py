import subprocess
import tkinter as tk
from tkinter import messagebox

def run_backup(direction):
    if direction == "backup":
        cmd = [
            "scp",
            "-r",
            "C:/Users/killi/OneDrive - Ynov/YNOV/Cours/Projet Infra/BackUpProject/sauvegarde",
            "backupuser@192.168.159.131:/home/backupuser/backups/"
        ]
        message_title = "Backup Successful"
        message_text = "La sauvegarde a été effectuée avec succès."
    elif direction == "retrieve":
        cmd = [
            "scp",
            "-r",
            "backupuser@192.168.159.131:/home/backupuser/backups/sauvegarde",
            "C:/Users/killi/OneDrive - Ynov/YNOV/Cours/Projet Infra/BackUpProject"
        ]
        message_title = "Retrieve Successful"
        message_text = "Les fichiers ont été récupérés avec succès."

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        messagebox.showinfo(message_title, message_text)
    else:
        messagebox.showerror("Error", "Une erreur s'est produite.")

# Création de l'interface utilisateur
root = tk.Tk()
root.title("Backup Interface")

# Définir la taille de la fenêtre sur 500x300 pixels
root.geometry("500x300")

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

# Centrer la fenêtre principale
center_window(root)

# Fonction appelée lorsque le bouton de sauvegarde est cliqué
def on_backup_click():
    run_backup("backup")

# Fonction appelée lorsque le bouton de récupération est cliqué
def on_retrieve_click():
    run_backup("retrieve")

# Création du bouton de sauvegarde
backup_button = tk.Button(root, text="Run Backup", command=on_backup_click)
backup_button.pack(pady=10)

# Création du bouton de récupération
retrieve_button = tk.Button(root, text="Retrieve Files", command=on_retrieve_click)
retrieve_button.pack(pady=10)

# Lancement de la boucle principale de l'interface utilisateur
root.mainloop()
