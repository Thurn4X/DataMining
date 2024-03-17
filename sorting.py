from pandas import json_normalize
import pandas as pd
import json
import os
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap


class ImageSorter(QWidget):
    def __init__(self, image_folder, metadata_file):
        super().__init__()
        self.image_folder = image_folder
        self.metadata_file = metadata_file
        self.metadata = self.load_metadata()
        self.image_files = self.get_image_files()
        self.current_image_index = 0

        self.init_ui()
        self.load_image()

    def load_metadata(self):
        with open(self.metadata_file, 'r') as f:
            return json.load(f)

    def get_image_files(self):
        return [file for file in os.listdir(self.image_folder) if
                file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    def init_ui(self):
        layout = QVBoxLayout()

        self.img_label = QLabel()
        layout.addWidget(self.img_label)

        like_button = QPushButton("J'aime")
        like_button.clicked.connect(self.favori)
        layout.addWidget(like_button)

        dislike_button = QPushButton("J'aime pas")
        dislike_button.clicked.connect(self.nonfavori)
        layout.addWidget(dislike_button)

        self.setLayout(layout)

    def load_image(self):
        image_path = os.path.join(self.image_folder, self.image_files[self.current_image_index])
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(250, 250)
        self.img_label.setPixmap(pixmap)

    def favori(self):
        image_name = self.image_files[self.current_image_index]
        for entry in self.metadata:
            if entry["nom"] == image_name:
                entry["favori"] = "yes"
                break
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=5)
        self.next_image()

    def nonfavori(self):
        image_name = self.image_files[self.current_image_index]
        for entry in self.metadata:
            if entry["nom"] == image_name:
                entry["favori"] = "no"
                break
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=5)
        self.next_image()

    def next_image(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
        self.load_image()

    def tri(self):
        data = json.load(open("image_metadata.json"))
        dataframe = json_normalize(data)
        print(dataframe)
