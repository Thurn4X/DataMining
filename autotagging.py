import os
import json
from tkinter import *
from PIL import Image, ImageTk
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.applications.inception_v3 import preprocess_input, decode_predictions


from tensorflow.keras.preprocessing import image
import numpy as np

# Chemin vers le dossier d'images et le fichier de métadonnées
image_folder = 'images/unsplash-images-collection'
metadata_file = 'image_metadata.json'

# Charger le modèle ResNet50 pré-entraîné sur ImageNet
model = InceptionV3(weights='imagenet')

def predict_tags(img_path):
    """Génère des tags pour une image en utilisant InceptionV3."""
    # Modifier target_size à (299, 299) pour InceptionV3
    img = image.load_img(img_path, target_size=(299, 299))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)
    # Retourne une liste des top 3 tags prédits
    return [tag[1] for tag in decode_predictions(preds, top=3)[0]]

# Charger les métadonnées existantes
def load_metadata():
    with open(metadata_file, 'r') as f:
        return json.load(f)

# Initialiser l'interface utilisateur
root = Tk()
img_label = Label(root)
img_label.pack(side="left", padx=10)

tag_entry = Entry(root, width=50)
tag_entry.pack(side="left", padx=10)

metadata = load_metadata()
image_files = [file for file in os.listdir(image_folder) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
current_image_index = [0]

def update_image():
    """Affiche l'image actuelle et génère des tags automatiquement."""
    global current_image_index, metadata, img_label
    image_path = os.path.join(image_folder, image_files[current_image_index[0]])
    img = Image.open(image_path)
    img = img.resize((250, 250), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    img_label.configure(image=img_tk)
    img_label.image = img_tk  # Gardez une référence

    # Générer et afficher les tags prédits
    predicted_tags = predict_tags(image_path)
    tag_entry.delete(0, END)  # Effacer le champ existant
    tag_entry.insert(0, ", ".join(predicted_tags))  # Insérer les tags prédits

def save_tag():
    """Sauvegarde le tag modifié ou confirmé par l'utilisateur."""
    tag = tag_entry.get().strip()
    image_name = image_files[current_image_index[0]]

    for entry in metadata:
        if entry["nom"] == image_name:
            entry["tags"] = tag.split(", ")
            break

    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=4)
    
    tag_entry.delete(0, END)
    next_image()

def next_image():
    current_image_index[0] = (current_image_index[0] + 1) % len(image_files)
    update_image()

def prev_image():
    current_image_index[0] = (current_image_index[0] - 1) % len(image_files)
    update_image()

save_button = Button(root, text="Save Tag", command=save_tag)
save_button.pack(side="left", padx=10)

next_button = Button(root, text="Next Image", command=next_image)
next_button.pack(side="right", padx=10)

prev_button = Button(root, text="Previous Image", command=prev_image)
prev_button.pack(side="right", padx=10)

update_image()
root.mainloop()
