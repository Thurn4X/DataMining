import json

# Charger le fichier de métadonnées
with open('image_metadata.json', 'r') as f:
    metadata = json.load(f)


import tkinter as tk
from PIL import Image, ImageTk
import os

# Créer la fenêtre Tkinter
root = tk.Tk()
root.title("Vérification des Couleurs Dominantes")

# Configurer la taille de la fenêtre si nécessaire
root.geometry("800x600")

# Label pour afficher l'image
img_label = tk.Label(root)
img_label.pack(side="left", padx=20)

# Canvas pour afficher la couleur dominante
color_canvas = tk.Canvas(root, width=100, height=100)
color_canvas.pack(side="left", padx=20)

images_path = 'images/images'


def rgb_to_hex(rgb):
    # Assurez-vous que rgb est un tuple pour la conversion hexadécimale
    return '#%02x%02x%02x' % rgb

# Fonction update_display ajustée pour traiter la couleur dominante comme une liste
def update_display(index):
    """Mettre à jour l'affichage avec l'image et la couleur dominante."""
    if index < len(metadata):
        meta = metadata[index]
        image_path = os.path.join(images_path, meta["nom"])
        img = Image.open(image_path)
        img = img.resize((250, 250))
        img_tk = ImageTk.PhotoImage(img)
        img_label.configure(image=img_tk)
        img_label.image = img_tk  # Garder une référence
        
        # Convertir la couleur dominante en format hexadécimal
        # meta["couleur_dominante"] est une liste, donc on la convertit en tuple
        color = rgb_to_hex(tuple(meta["couleur_dominante"]))
        color_canvas.create_rectangle(0, 0, 100, 100, fill=color, outline=color)
        
        # Mise à jour pour la prochaine image après un délai
        root.after(2000, update_display, index + 1)  # Attendre 2 secondes

update_display(0)  # Commencer avec la première image
root.mainloop()