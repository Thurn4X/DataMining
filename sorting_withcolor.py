import json
import os
from tkinter import *

from PIL import Image, ImageTk


# Fonction pour convertir les valeurs RGB en couleur hexadécimale
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)


# Chemin vers le dossier d'images et le fichier de métadonnées
image_folder = 'images/images'
metadata_file = 'image_metadata.json'


# Charger les métadonnées existantes
def load_metadata():
    with open(metadata_file, 'r') as f:
        return json.load(f)


# Initialiser l'interface utilisateur
root = Tk()
img_label = Label(root)
img_label.pack(side="left", padx=10)

# Canvas pour afficher la couleur dominante
color_display = Canvas(root, width=50, height=50)
color_display.pack(side="left", padx=10)

metadata = load_metadata()
image_files = [file for file in os.listdir(image_folder) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
current_image_index = [0]


# Afficher l'image actuelle et sa couleur dominante
def update_image():
    image_path = os.path.join(image_folder, image_files[current_image_index[0]])
    img = Image.open(image_path)
    img = img.resize((250, 250), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    img_label.configure(image=img_tk)
    img_label.image = img_tk  # Gardez une référence pour éviter le garbage collector

    # Afficher la couleur dominante
    dominant_color = [entry for entry in metadata if entry['nom'] == image_files[current_image_index[0]]][0][
        'couleur_dominante']
    hex_color = rgb_to_hex(dominant_color)
    color_display.create_rectangle(0, 0, 50, 50, fill=hex_color, outline=hex_color)


# Ajouter un tag à l'image actuelle et sauvegarder les métadonnées
def favori():
    image_name = image_files[current_image_index[0]]  # Nom de l'image actuelle

    # Chercher l'entrée correspondante dans les métadonnées grâce au nom de l'image
    # et ajouter le tag à la liste des tags
    for entry in metadata:
        if entry["nom"] == image_name:
            entry["favori"] = "yes"
            break
    # Sauvegarder les métadonnées mises à jour dans le fichier JSON
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=5)
    next_image()


# Fonctions pour naviguer entre les images
def next_image():
    current_image_index[0] = (current_image_index[0] + 1) % len(image_files)
    update_image()


def prev_image():
    current_image_index[0] = (current_image_index[0] - 1) % len(image_files)
    update_image()


def nonfavori():
    image_name = image_files[current_image_index[0]]  # Nom de l'image actuelle

    # Chercher l'entrée correspondante dans les métadonnées grâce au nom de l'image
    # et ajouter le tag à la liste des tags
    for entry in metadata:
        if entry["nom"] == image_name:
            entry["favori"] = "no"
            break
    # Sauvegarder les métadonnées mises à jour dans le fichier JSON
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=5)
    next_image()


# Boutons pour sauvegarder les préférences et naviguer entre les images
like_button = Button(root, text="J'aime", command=favori)
like_button.pack(side="left", padx=10)
dislike_button = Button(root, text="J'aime pas", command=nonfavori)
dislike_button.pack(side="left", padx=10)

# Les fonctions next_image et prev_image restent inchangées

update_image()
root.mainloop()
