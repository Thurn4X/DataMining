from pandas import json_normalize
import pandas as pd
import json

data = json.load(open("image_metadata.json"))
dataframe = json_normalize(data)
print(dataframe)



import os
from tkinter import *
from PIL import Image, ImageTk
import json

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
img_label.pack()


metadata = load_metadata()
# on prend les images qui sont dans le dossier et qui ont une extension .png, .jpg, .jpeg, .gif
image_files = [file for file in os.listdir(image_folder) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
# on prend l'index de l'image actuelle pour parcourir les images plus tard
current_image_index = [0]

# Afficher l'image actuelle
def update_image():
    image_path = os.path.join(image_folder, image_files[current_image_index[0]])
    img = Image.open(image_path)
    img = img.resize((250, 250), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    img_label.configure(image=img_tk)
    img_label.image = img_tk


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

# Boutons pour sauvegarder les tags et naviguer entre les images
like_button = Button(root, text="J'aime", command=favori)
like_button.pack()
dislike_button = Button(root, text="J'aime pas", command=nonfavori)
dislike_button.pack()

# Fonctions pour naviguer entre les images
def next_image():
    current_image_index[0] = (current_image_index[0] + 1) % len(image_files)
    update_image()

def prev_image():
    current_image_index[0] = (current_image_index[0] - 1) % len(image_files)
    update_image()

update_image()
root.mainloop()
