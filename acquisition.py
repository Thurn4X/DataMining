import os
import zipfile

import gdown


def acquire():
    # URL de téléchargement direct Google Drive
    # pour le gros dataset non tagged
    url = 'https://drive.google.com/uc?id=16rYRrxUXpGyPWVq5uhgYzNlZd6hsGX7-'
    # pour le petit dataset pokemon
    # url = 'https://drive.google.com/uc?id=1yfy6XXv0VikxR8xTuz-xQts_MmGWRDUy'
    # Chemin de destination
    output = 'dataset.zip'

    # Télécharge le fichier depuis l'URL
    gdown.download(url, output, quiet=False)

    # Décompresse le fichier dans le dossier 'img'

    with zipfile.ZipFile(output, 'r') as zip_ref:
        zip_ref.extractall('images')
    # Supprime le fichier zip si désiré
    os.remove(output)
