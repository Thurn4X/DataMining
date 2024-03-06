import os
import json
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap, QIcon
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.applications.inception_v3 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np


def predict_tags(img_path):
    """Génère des tags pour une image en utilisant InceptionV3."""
    # Modifier target_size à (299, 299) pour InceptionV3
    img = image.load_img(img_path, target_size=(299, 299))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    model = InceptionV3(weights='imagenet')
    preds = model.predict(x)
    # Retourne une liste des top 3 tags prédits
    return [tag[1] for tag in decode_predictions(preds, top=3)[0]]


class ImageTagger(QWidget):
    def __init__(self, image_folder, metadata_file):
        super().__init__()
        self.setWindowTitle("Image Tagger")
        self.metadata_file = metadata_file
        self.metadata = self.load_metadata()
        self.image_folder = image_folder
        self.image_files = [file for file in os.listdir(image_folder) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        self.current_image_index = 0

        self.img_label = QLabel()
        self.tag_entry = QLineEdit()

        self.save_button = QPushButton("Save Tag")
        self.save_button.clicked.connect(self.save_tag)

        self.next_button = QPushButton("Next Image")
        self.next_button.clicked.connect(self.next_image)

        self.prev_button = QPushButton("Previous Image")
        self.prev_button.clicked.connect(self.prev_image)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.img_label)
        hbox1.addWidget(self.tag_entry)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.prev_button)
        hbox2.addWidget(self.next_button)
        hbox2.addWidget(self.save_button)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)

        self.update_image()

    def update_image(self):
        """Affiche l'image actuelle et génère des tags automatiquement."""
        image_path = os.path.join(self.image_folder, self.image_files[self.current_image_index])
        pixmap = QPixmap(str(image_path))
        self.img_label.setPixmap(pixmap)
        # Générer et afficher les tags prédits
        predicted_tags = predict_tags(image_path)
        self.tag_entry.setText(", ".join(predicted_tags))

    def save_metadata(self):
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=4)

    def load_metadata(self):
        with open(self.metadata_file, 'r') as f:
            return json.load(f)

    def save_tag(self):
        tag = self.tag_entry.text().strip()
        if tag:
            image_name = self.image_files[self.current_image_index]
            for entry in self.metadata:
                image_key = next(
                    (key for key in entry.keys() if isinstance(entry[key], str) and entry[key].endswith(image_name)),
                    None)
                if image_key:
                    if "tags" not in entry:
                        entry["tags"] = []
                    for new_tag in tag.split(", "):
                        if new_tag not in entry["tags"]:
                            entry["tags"].append(new_tag)
                    break
            else:
                self.metadata.append({image_name: image_name, "tags": [tag]})
            self.save_metadata()
            self.tag_entry.clear()

    def next_image(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
        self.update_image()

    def prev_image(self):
        self.current_image_index = (self.current_image_index - 1) % len(self.image_files)
        self.update_image()
