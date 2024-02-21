import pandas as pd
import json

# Chemin vers le fichier CSV
csv_path = 'pokemon.csv'
# Lire le fichier CSV
df = pd.read_csv(csv_path)

# Créer un dictionnaire pour mapper le nom de chaque Pokémon à ses types
pokemon_types = {row['Name'].lower(): [row['Type1'], row['Type2']] for index, row in df.iterrows()}

# Chemin vers le fichier JSON de métadonnées
metadata_path = 'image_metadata.json'

# Charger les métadonnées existantes
with open(metadata_path, 'r') as file:
    metadata = json.load(file)

for info in metadata:
    # Extraire le nom de l'image (le nom du fichier correspond au nom du Pokémon)
    pokemon_name = info['nom'].split('.')[0].lower()
    
    # Vérifier si le nom est dans le dictionnaire pokemon_types
    if pokemon_name in pokemon_types:
        # Récupérer la liste des types pour ce Pokémon
        types_list = pokemon_types[pokemon_name]
        
        # Filtrer les types pour exclure les valeurs manquantes ou les chaînes vides
        true_types = []
        for t in types_list:
            # Regarder si la valeur n'est pas nulle et n'est pas une chaîne vide
            if pd.notna(t) and t != '':
                true_types.append(t)
        
        # Ajouter les types filtrés à la liste des tags pour ce Pokémon
        info['tags'].extend(true_types)

# Sauvegarder les métadonnées mises à jour dans le fichier JSON
with open(metadata_path, 'w') as file:
    json.dump(metadata, file, indent=4)
