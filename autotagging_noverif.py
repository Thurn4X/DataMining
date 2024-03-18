import json
import os

import numpy as np
from sentence_transformers import SentenceTransformer, util
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
    return [tag[1] for tag in decode_predictions(preds, top=1)[0]]


def associated_theme(tag, model_language, theme_embeddings):
    # Charger le modèle de transformation de phrases

    tag_embedding = model_language.encode([tag], convert_to_tensor=True)
    max_similarity = -1
    assigned_theme = "other"
    for theme, theme_embedding in theme_embeddings.items():
        similarity = util.pytorch_cos_sim(tag_embedding, theme_embedding).max()
        if similarity > max_similarity:
            max_similarity = similarity
            assigned_theme = theme
    return assigned_theme


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

    model_language = SentenceTransformer('all-MiniLM-L6-v2')

    # Thèmes et mots-clés correspondants
    themes = {
        "nature": ["forest", "greenhouse", "boathouse", "river", "mountain", "sky", "lake", "ocean", "canoe", "geyser",
                   "flower", "maze", "alp", "dam", "snowplow", "desert", "valley", "hay", "bubble"],
        "sports": ["mountain_bike", "soccer", "basketball", "tennis", "ball", "running", "swimming", "cycling"],
        "art": ["vase", "painting", "sculpture", "drawing", "museum", "gallery", "street art", "dome"],
        "animal": ["animal", "dog", "cat", "bird", "fish", "wildlife", "honeycomb", ],
        "object": ["table", "balloon", "object", "chair", "lamp", "computer", "basket"],
        "food": ["hotdog", "food", "vegetable", "fruit", "meal", "dessert", "drink", "plate", "matchstick", "cup",
                 "parachute", "rotisserie", "barometer"],
        "clothes": ["shirt", "cloak", "sock", "pants", "dress", "hat", "shoes", "stockings"],
        "transportation": ["bridge", "car", "train", "airplane", "bike", "boat", "road", "highway"],
        "urban": ["street", "alley", "urban", "city life", "market", "park", "window", "uniform", "solar_dish", "fence",
                  "stupa", "palace"],
        # Add more themes as needed
    }

    # Embeddings pour les thèmes
    theme_embeddings = {theme: model_language.encode(keywords, convert_to_tensor=True) for theme, keywords in
                        themes.items()}

    for image_name in image_files:
        image_path = os.path.join(image_folder, image_name)
        # Générer des tags prédits pour l'image
        predicted_tags = predict_tags(image_path, model)
        predicted_theme = associated_theme(predicted_tags[0], model_language, theme_embeddings)
        # Trouver l'entrée correspondante dans les métadonnées et mettre à jour les tags
        for entry in metadata:
            if entry["nom"] == image_name:
                entry["tags"] = predicted_theme
                break

    # Sauvegarder les métadonnées mises à jour
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=4)
