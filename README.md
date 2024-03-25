# Projet de recommandation d'images

## Description
Ce projet a pour but de recommander des images à un utilisateur en fonction de ses préférences. Pour cela, nous avons utilisé un jeu de données contenant des images et des tags associés à ces images. Nous avons utilisé une méthode de factorisation de matrices pour prédire les tags associés à une image non taggée. Nous avons également utilisé une méthode de clustering pour regrouper les images en fonction de leurs tags.

Il fonctionne en 5 étapes :
1. Téléchargement des images
2. Création d'un fichier JSON pour contenir les informations générées
3. Reconnaissance d'objets sur les images
4. Tri des images favorites/non favorites
5. Recommandation d'images

Le projet peut à la fois être utilisé avec le notebook Projet_DataMining.ipynb ou avec le fichier main.py qui lance une interface graphique.

## Installation
Nous avons utilisé les librairies suivantes :
- gdown
- pillow
- scikit-learn
- tensorflow
- sentence-transformers
- ipywidgets
- pandas

Pour utiliser la version graphique, il faut installer en plus :
- PyQt5

Pour utiliser la version notebook, il faut installer en plus :
- jupyter

Pour installer les librairies, il suffit de lancer la commande suivante :
```bash
pip install -r requirements.txt
```