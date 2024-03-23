import json
import os

import numpy as np
from PIL import Image, ExifTags
from sklearn.cluster import MiniBatchKMeans

import webcolors

def closest_color(requested_color):
    min_colors = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]

def find_dominant_color(image_path, n_clusters=2):
    img = Image.open(image_path).convert('RGBA')
    img = img.resize((50, 50))
    numarray = np.array(img)
    numarray = numarray[:, :, :3][numarray[:, :, 3] > 0]

    clusters = MiniBatchKMeans(n_clusters=n_clusters)
    clusters.fit(numarray)

    counts = np.bincount(clusters.labels_)
    most_frequent = clusters.cluster_centers_[counts.argmax()]

    closest_name = closest_color(tuple(int(c) for c in most_frequent))

    return tuple(int(c) for c in most_frequent), closest_name



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


def create_metadata():
    # Chemin vers le dossier d'images et le fichier de métadonnées
    images_path = 'images/unsplash-images-collection'
    metadata_file = 'image_metadata.json'
    metadata = []

    for image_file in os.listdir(images_path):
        image_path = os.path.join(images_path, image_file)

        img = Image.open(image_path)
        # Extraction des données Exif
        exif_data = get_exif_data(img)
        dominant_color = find_dominant_color(image_path)  # Trouver la couleur dominante

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
