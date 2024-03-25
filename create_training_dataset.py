import json
import os
import time

import numpy as np
import pandas as pd
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from sklearn.linear_model import Perceptron
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split



class ImageRecommender(QWidget):
    def __init__(self, image_folder):
        super().__init__()
        self.img_label = None
        self.image_folder = image_folder
        self.data = self.load_data()
        self.dataframe = self.create_dataframe()
        self.models = self.train_models()
        self.recommended_images = self.get_recommendations()
        self.init_ui()
        self.show_images()

    @staticmethod
    def load_data():
        with open("image_metadata.json", "r") as file:
            data = json.load(file)
        return data

    def create_dataframe(self):
        dataframe = pd.json_normalize(self.data)
        dataframe['aire_image'] = dataframe['taille'].apply(lambda x: x[0] * x[1])

        # Initialiser les DataFrames des thèmes et des tags avec des valeurs par défaut (aucun thème/tag)
        themes_df = pd.DataFrame(index=dataframe.index)
        tags_df = pd.DataFrame(index=dataframe.index)

        # Encodage One-Hot des thèmes s'ils existent
        if 'theme' in dataframe.columns:
            mlb_theme = MultiLabelBinarizer()
            themes_encoded = mlb_theme.fit_transform(dataframe['theme'].apply(lambda x: [x] if isinstance(x, str) else x))
            themes_df = pd.DataFrame(themes_encoded, columns=mlb_theme.classes_, index=dataframe.index)

        # Encodage One-Hot des tags manuels s'ils existent
        if 'tags' in dataframe.columns:
            mlb_tags = MultiLabelBinarizer()
            tags_encoded = mlb_tags.fit_transform(dataframe['tags'].apply(lambda x: [x] if isinstance(x, str) else x))
            tags_df = pd.DataFrame(tags_encoded, columns=mlb_tags.classes_, index=dataframe.index)

        # Fusionner les DataFrame des thèmes et des tags
        all_tags_df = pd.concat([themes_df, tags_df], axis=1, sort=False).fillna(0).astype(int)

        format_df = pd.get_dummies(dataframe['format'], prefix='format')
        orientation_df = pd.get_dummies(dataframe['orientation'], prefix='orientation')
        color_df = pd.get_dummies(dataframe['couleur_dominante'].apply(lambda x: x[-1] if isinstance(x, list) and len(x) > 1 else 'unknown'), prefix='color')

        # Concaténer toutes les caractéristiques
        all_final_df = pd.concat([all_tags_df, format_df, orientation_df, color_df, dataframe[['aire_image']]], axis=1)

        # Séparer les images évaluées et non évaluées
        dataframe_evalue = dataframe[dataframe['favori'] != 'n/a']
        dataframe_non_evalue = dataframe[dataframe['favori'] == 'n/a']
        labels_evalue = dataframe_evalue['favori'].map({'yes': 1, 'no': 0})

        # Sélectionner les caractéristiques pour les images évaluées et non évaluées
        X_train = all_final_df.loc[dataframe_evalue.index]
        y_train = labels_evalue
        X_test = all_final_df.loc[dataframe_non_evalue.index]

        return X_train, X_test, y_train, dataframe_non_evalue, all_final_df.columns.to_list()



    def train_models(self):
        X_train, X_test, y_train, dataframe_non_evalue, feature_names = self.create_dataframe()  # Mise à jour pour inclure feature_names

        svc = SVC(probability=True)
        perceptron = Perceptron()
        decision_tree = DecisionTreeClassifier()

        X_train_eval, X_test_eval, y_train_eval, y_test_eval = train_test_split(
            X_train, y_train, test_size=0.2, random_state=50)

        svc.fit(X_train_eval, y_train_eval)
        perceptron.fit(X_train_eval, y_train_eval)
        decision_tree.fit(X_train_eval, y_train_eval)

        for model, name in zip([svc, perceptron, decision_tree], ["SVC", "Perceptron", "Decision Tree"]):
            y_pred = model.predict(X_test_eval)
            print(f"--- {name} ---")
            print("Matrice de confusion :\n", confusion_matrix(y_test_eval, y_pred))
            print("Précision :", accuracy_score(y_test_eval, y_pred))
            print("Rapport de classification :\n", classification_report(y_test_eval, y_pred))

        importances = decision_tree.feature_importances_
        sorted_indices = np.argsort(importances)[::-1]
        print("Importance des caractéristiques :")
        for idx in sorted_indices[:20]:  # Afficher les 10 caractéristiques les plus importantes
            print(f"{feature_names[idx]}: {importances[idx]:.4f}")

        return svc, perceptron, decision_tree


    def get_recommendations(self):
        _, X_test, _, dataframe_non_evalue, _ = self.create_dataframe()  # Correction pour correspondre à la structure retournée
        svc, _, decision_tree = self.models

        predictions_tree = decision_tree.predict(X_test)
        indices_liked = np.where(predictions_tree == 1)[0]
        top_n = 10
        recommended_indices = indices_liked[:top_n]
        recommended_images_tree = dataframe_non_evalue.iloc[recommended_indices]['nom'].values

        return recommended_images_tree


    def init_ui(self):
        layout = QVBoxLayout()
        self.img_label = QLabel()
        layout.addWidget(self.img_label)
        self.setLayout(layout)

    def show_images(self):
        for image_name in self.recommended_images:
            image_path = os.path.join(self.image_folder, image_name)
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(250, 250)
            self.img_label.setPixmap(pixmap)
            self.show()
            QApplication.processEvents()
            time.sleep(2)
