from PIL import Image, ExifTags
import os
import json
from sklearn.cluster import MiniBatchKMeans
import numpy as np


# Chemin vers le dossier d'images et le fichier de métadonnées
images_path = 'images/unsplash-images-collection'
metadata_file = 'image_metadata.json'
metadata = []





def find_dominant_color(image_path, n_clusters=2):
    img = Image.open(image_path).convert('RGBA')  # Convertir en RGBA
    img = img.resize((50, 50))  # Optionnel: Redimensionner

    # Convertir l'image RGBA en une array numpy, ignorer les pixels complètement transparents
    numarray = np.array(img)
    numarray = numarray[:, :, :3][numarray[:, :, 3] > 0]  # Ignorer les pixels transparents

    clusters = MiniBatchKMeans(n_clusters=n_clusters)
    clusters.fit(numarray)

    counts = np.bincount(clusters.labels_)
    most_frequent = clusters.cluster_centers_[counts.argmax()]

    return tuple(int(c) for c in most_frequent)


# Fonction pour avoir l'orientation de l'image
def get_image_orientation(img):
    if img.width > img.height:
        return "paysage"
    elif img.width < img.height:
        return "portrait"
    else:
        return "carre"

# Fonction pour extraire les données Exif
def get_exif_data(img):
    exif_data = {}
    raw_exif = img._getexif()
    if raw_exif:
        for tag, value in raw_exif.items():
            decoded_tag = ExifTags.TAGS.get(tag, tag)
            exif_data[decoded_tag] = value
    return exif_data


for image_file in os.listdir(images_path):
    #print(f"Traitement de : {image_file}")
    image_path = os.path.join(images_path, image_file)

    img = Image.open(image_path)
    # Extraction des données Exif
    exif_data = get_exif_data(img)
    dominant_color = find_dominant_color(image_path)  # Trouver la couleur dominante

    print(exif_data)
    metadata.append({
        "nom": image_file,
        "taille": img.size,
        "format": img.format,
        "orientation": get_image_orientation(img),
        "exif": exif_data,  # Ajoutez les données Exif ici
        "couleur_dominante": dominant_color,  # Ajouter la couleur dominante aux métadonnées

        "tags": [],
        "favori": "n/a"
    })

if metadata:
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=4)
    print("Métadonnées enregistrées.")
else:
    print("Aucune métadonnée à enregistrer.")
