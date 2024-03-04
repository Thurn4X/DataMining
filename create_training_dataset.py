import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
import json
import numpy as np

# Charger le dataset
with open("image_metadata.json", "r") as file:
    data = json.load(file)

# Créer le DataFrame
dataframe = pd.json_normalize(data)

# Calcul de l'aire de l'image à partir de la colonne 'taille'
dataframe['aire_image'] = dataframe['taille'].apply(lambda x: x[0] * x[1])

# Encodage One-Hot des tags pour l'ensemble du dataset
mlb = MultiLabelBinarizer()
tags_encoded = mlb.fit_transform(dataframe['tags'])
tags_df = pd.DataFrame(tags_encoded, columns=mlb.classes_)

# Encodage One-Hot pour 'format' et 'orientation' pour l'ensemble du dataset
format_df = pd.get_dummies(dataframe['format'], prefix='format')
orientation_df = pd.get_dummies(dataframe['orientation'], prefix='orientation')


# Exemple de création de colonnes pour les composantes RGB de la couleur dominante
dataframe['dominant_color_r'] = dataframe['couleur_dominante'].apply(lambda x: x[0] if isinstance(x, list) else 0)
dataframe['dominant_color_g'] = dataframe['couleur_dominante'].apply(lambda x: x[1] if isinstance(x, list) else 0)
dataframe['dominant_color_b'] = dataframe['couleur_dominante'].apply(lambda x: x[2] if isinstance(x, list) else 0)

# Ajouter les colonnes de couleur dominante au DataFrame final
all_final_df = pd.concat([
    tags_df,
    format_df,
    orientation_df,
    dataframe[['aire_image', 'dominant_color_r', 'dominant_color_g', 'dominant_color_b']]
], axis=1)



# Séparer les images évaluées et non évaluées
dataframe_evalue = dataframe[dataframe['favori'] != 'n/a']
dataframe_non_evalue = dataframe[dataframe['favori'] == 'n/a']

# Préparation des labels pour le set évalué
labels_evalue = dataframe_evalue['favori'].map({'yes': 1, 'no': 0})

# Sélectionner les caractéristiques pour les images évaluées uniquement pour l'entraînement
X_train = all_final_df.loc[dataframe_evalue.index]
print(X_train)
y_train = labels_evalue

# Sélectionner les caractéristiques pour les images non évaluées pour la prédiction
X_test = all_final_df.loc[dataframe_non_evalue.index]
from sklearn.model_selection import train_test_split

# Diviser les données évaluées en ensembles d'entraînement et de test
X_train_eval, X_test_eval, y_train_eval, y_test_eval = train_test_split(
    X_train, y_train, test_size=0.2, random_state=50)






from sklearn.svm import SVC
from sklearn.linear_model import Perceptron
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report


# Initialisation des modèles
svc = SVC(probability=True)  # Pour SVC, activez la probabilité pour obtenir des scores de prédiction
perceptron = Perceptron()
decision_tree = DecisionTreeClassifier()

# Entraînement des modèles sur l'ensemble d'entraînement évalué
svc.fit(X_train_eval, y_train_eval)
perceptron.fit(X_train_eval, y_train_eval)
decision_tree.fit(X_train_eval, y_train_eval)



# Faire des prédictions sur l'ensemble de test évalué
predictions_svc_eval = svc.predict(X_test_eval)
predictions_perceptron_eval = perceptron.predict(X_test_eval)
predictions_tree_eval = decision_tree.predict(X_test_eval)

# Afficher la précision et d'autres métriques pour chaque modèle
print("Classification Report pour SVC:")
print(classification_report(y_test_eval, predictions_svc_eval))

print("Classification Report pour Perceptron:")
print(classification_report(y_test_eval, predictions_perceptron_eval))

print("Classification Report pour Decision Tree:")
print(classification_report(y_test_eval, predictions_tree_eval))


#################### recommandation par svc ############################

# Obtenir les probabilités de la classe positive (par exemple, "aimé" ou 1)
probabilities_svc = svc.predict_proba(X_test)[:, 1]
# Obtenir les indices des images triées par probabilité décroissante
indices_sorted_svc = np.argsort(probabilities_svc)[::-1]

# Sélectionner le top N images
top_n = 10 
top_indices_svc = indices_sorted_svc[:top_n]

# Récupérer les noms des images pour les top-N recommandations
recommended_images_svc = dataframe_non_evalue.iloc[top_indices_svc]['nom'].values
print("Images recommandées par SVC :", recommended_images_svc)

#################### recommandation par decision tree ############################
# Faire des prédictions sur les données non évaluées
predictions_tree = decision_tree.predict(X_test)
# Trouver les indices des images prédites comme aimées ("yes")
indices_liked = np.where(predictions_tree == 1)[0]

# Noms des caractéristiques
feature_names = all_final_df.columns

# Afficher l'importance avec les noms des caractéristiques
importances = decision_tree.feature_importances_
importances_with_names = zip(feature_names, importances)
sorted_importances = sorted(importances_with_names, key=lambda x: x[1], reverse=True)

for name, importance in sorted_importances:
    print(f"{name}: {importance}")

top_n = 10  # Nombre d'images recommandées
recommended_indices = indices_liked[:top_n]

# Récupérer les noms des images recommandées
recommended_images_tree = dataframe_non_evalue.iloc[recommended_indices]['nom'].values

print("Images recommandées par Decision Tree :", recommended_images_tree)



import tkinter as tk
from PIL import Image, ImageTk
import time
import os

# Fonction pour afficher une image dans la fenêtre Tkinter
def show_image(image_path):
    img = Image.open(image_path)
    img = img.resize((250, 250), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    img_label.configure(image=img_tk)
    img_label.image = img_tk
    root.update_idletasks()
    root.update()

# Créer la fenêtre Tkinter
root = tk.Tk()
img_label = tk.Label(root)
img_label.pack()

# Définir le dossier contenant les images et les noms des images recommandées
image_folder = 'images/unsplash-images-collection'
recommended_images = recommended_images_tree  # Supposons que ceci est la liste des noms d'images recommandées

# Afficher chaque image recommandée
for image_name in recommended_images:
    image_path = os.path.join(image_folder, image_name)
    show_image(image_path)
    time.sleep(2)  # Attendre 2 secondes avant de passer à l'image suivante

root.mainloop()

