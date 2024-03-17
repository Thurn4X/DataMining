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

        mlb = MultiLabelBinarizer()
        tags_encoded = mlb.fit_transform(dataframe['tags'])
        tags_df = pd.DataFrame(tags_encoded, columns=mlb.classes_)

        format_df = pd.get_dummies(dataframe['format'], prefix='format')
        orientation_df = pd.get_dummies(dataframe['orientation'], prefix='orientation')

        dataframe['dominant_color_r'] = dataframe['couleur_dominante'].apply(
            lambda x: x[0] if isinstance(x, list) else 0)
        dataframe['dominant_color_g'] = dataframe['couleur_dominante'].apply(
            lambda x: x[1] if isinstance(x, list) else 0)
        dataframe['dominant_color_b'] = dataframe['couleur_dominante'].apply(
            lambda x: x[2] if isinstance(x, list) else 0)

        all_final_df = pd.concat([
            tags_df,
            format_df,
            orientation_df,
            dataframe[['aire_image', 'dominant_color_r', 'dominant_color_g', 'dominant_color_b']]
        ], axis=1)

        dataframe_evalue = dataframe[dataframe['favori'] != 'n/a']
        dataframe_non_evalue = dataframe[dataframe['favori'] == 'n/a']

        labels_evalue = dataframe_evalue['favori'].map({'yes': 1, 'no': 0})

        X_train = all_final_df.loc[dataframe_evalue.index]
        y_train = labels_evalue

        X_test = all_final_df.loc[dataframe_non_evalue.index]

        return X_train, X_test, y_train, dataframe_non_evalue

    def train_models(self):
        X_train, _, y_train, _ = self.dataframe

        svc = SVC(probability=True)
        perceptron = Perceptron()
        decision_tree = DecisionTreeClassifier()

        svc.fit(X_train, y_train)
        perceptron.fit(X_train, y_train)
        decision_tree.fit(X_train, y_train)

        return svc, perceptron, decision_tree

    def get_recommendations(self):
        _, X_test, _, dataframe_non_evalue = self.dataframe
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
