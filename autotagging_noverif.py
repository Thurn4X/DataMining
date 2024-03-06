import os
import json
from PIL import Image
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np

# Chemin vers le dossier d'images et le fichier de métadonnées
image_folder = 'images/unsplash-images-collection'
metadata_file = 'image_metadata.json'

# Charger le modèle MobileNetV2 pré-entraîné sur ImageNet
model = MobileNetV2(weights='imagenet')

def predict_tags(img_path):
    """Génère des tags pour une image en utilisant MobileNetV2."""
    img = image.load_img(img_path, target_size=(224, 224))
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

metadata = load_metadata()
image_files = [file for file in os.listdir(image_folder) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

def update_metadata_with_tags():
    """Mise à jour des métadonnées avec des tags prédits pour chaque image."""
    for image_name in image_files:
        image_path = os.path.join(image_folder, image_name)
        # Générer des tags prédits pour l'image
        predicted_tags = predict_tags(image_path)
        # Trouver l'entrée correspondante dans les métadonnées et mettre à jour les tags
        for entry in metadata:
            if entry["nom"] == image_name:
                entry["tags"] = predicted_tags
                break
    
    # Sauvegarder les métadonnées mises à jour
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=4)

if __name__ == "__main__":
    update_metadata_with_tags()
