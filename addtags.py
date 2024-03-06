import os
from tkinter import *
from PIL import Image, ImageTk
import json


# Charger les métadonnées existantes
def load_metadata(metadata_file):
    with open(metadata_file, 'r') as f:
        return json.load(f)

# Afficher l'image actuelle
def update_image(image_folder, image_files, current_image_index, img_label):
    image_path = os.path.join(image_folder, image_files[current_image_index[0]])
    img = Image.open(image_path)
    img = img.resize((250, 250), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    img_label.configure(image=img_tk)
    img_label.image = img_tk

# Ajouter un tag à l'image actuelle et sauvegarder les métadonnées
def save_tag(tag_entry, image_files, current_image_index, metadata, metadata_file):
    # Récupérer le tag saisi et le nom de l'image actuelle
    tag = tag_entry.get().strip()  # Nettoyer le tag saisi
    image_name = image_files[current_image_index[0]]  # Nom de l'image actuelle

    # Chercher l'entrée correspondante dans les métadonnées grâce au nom de l'image
    # et ajouter le tag à la liste des tags
    for entry in metadata:
        if entry["nom"] == image_name:
            if "tags" not in entry:  # Si l'entrée n'a pas de clé "tags", l'ajouter
                entry["tags"] = []
            entry["tags"].append(tag)  # Ajouter le tag à la liste des tags pour cette image
            break

   # Sauvegarder les métadonnées mises à jour dans le fichier JSON
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=4)

    tag_entry.delete(0, END)  # Effacer le champ de saisie

# Fonctions pour naviguer entre les images
def next_image(image_folder, image_files, current_image_index, img_label):
    current_image_index[0] = (current_image_index[0] + 1) % len(image_files)
    update_image(image_folder, image_files, current_image_index, img_label)

def prev_image(image_folder, image_files, current_image_index, img_label):
    current_image_index[0] = (current_image_index[0] - 1) % len(image_files)
    update_image(image_folder, image_files, current_image_index, img_label)

def window():
    # Chemin vers le dossier d'images et le fichier de métadonnées
    image_folder = 'images/unsplash-images-collection'
    metadata_file = 'image_metadata.json'

    # Initialiser l'interface utilisateur
    root = Tk()
    img_label = Label(root)
    img_label.pack()

    tag_entry = Entry(root)
    tag_entry.pack()

    metadata = load_metadata(metadata_file)
    # on prend les images qui sont dans le dossier et qui ont une extension .png, .jpg, .jpeg, .gif
    image_files = [file for file in os.listdir(image_folder) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    # on prend l'index de l'image actuelle pour parcourir les images plus tard
    current_image_index = [0]

    # Boutons pour sauvegarder les tags et naviguer entre les images
    save_button = Button(root, text="Save Tag", command=lambda: save_tag(tag_entry, image_files, current_image_index, metadata, metadata_file))
    save_button.pack()

    next_button = Button(root, text="Next Image", command=lambda: next_image(image_folder, image_files, current_image_index, img_label))
    next_button.pack()
    prev_button = Button(root, text="Previous Image", command=lambda: prev_image(image_folder, image_files, current_image_index, img_label))
    prev_button.pack()

    update_image(image_folder, image_files, current_image_index, img_label)
    root.mainloop()