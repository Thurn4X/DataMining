import json
import os

import numpy as np
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.applications.inception_v3 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image


def predict_tags(img_path, model):
    img = image.load_img(img_path, target_size=(299, 299))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    # Retourne une liste des top 3 tags prédits
    return [tag[1] for tag in decode_predictions(preds, top=5)[0]]


# Charger les métadonnées existantes
def load_metadata():
    metadata_file = 'image_metadata.json'
    with open(metadata_file, 'r') as f:
        return json.load(f)


def update_metadata_with_tags():
    # Chemin vers le dossier d'images et le fichier de métadonnées
    image_folder = 'images/unsplash-images-collection'

    """Mise à jour des métadonnées avec des tags prédits pour chaque image."""
    metadata = load_metadata()
    metadata_file = 'image_metadata.json'
    image_files = [file for file in os.listdir(image_folder) if
                   file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    model = InceptionV3(weights='imagenet')
    for image_name in image_files:
        image_path = os.path.join(image_folder, image_name)
        # Générer des tags prédits pour l'image
        predicted_tags = predict_tags(image_path, model)
        # Trouver l'entrée correspondante dans les métadonnées et mettre à jour les tags
        for entry in metadata:
            if entry["nom"] == image_name:
                entry["tags"] = predicted_tags
                break

    # Sauvegarder les métadonnées mises à jour
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=4)
