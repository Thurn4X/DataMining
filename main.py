import acquisition
import metadata
import addtags
import sorting
import create_training_dataset

import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recommendation")
        self.setGeometry(100, 100, 600, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.image_count_label = QLabel("Nombre d'images: 0")
        layout.addWidget(self.image_count_label, alignment=Qt.AlignHCenter)

        self.download_button = QPushButton("Téléchargement des images")
        self.download_button.clicked.connect(self.download_images)
        layout.addWidget(self.download_button)

        warning_label = QLabel("Attention:\nCette opération efface les images déjà téléchargées et les métadonnées existantes.")
        # Make the warning label bold
        font = warning_label.font()
        font.setBold(True)
        warning_label.setFont(font)
        warning_label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(warning_label)

        self.add_tags_button = QPushButton("Ajout de tags")
        self.add_tags_button.clicked.connect(self.open_addtags)
        layout.addWidget(self.add_tags_button)

        self.sort_images_button = QPushButton("Tri des images")
        self.sort_images_button.clicked.connect(sorting.tri)
        layout.addWidget(self.sort_images_button)

        self.create_dataset_button = QPushButton("Création du jeu de données")
        self.create_dataset_button.clicked.connect(create_training_dataset.create)
        layout.addWidget(self.create_dataset_button)

        self.update_image_count()

    def open_addtags(self):
        self.w = addtags.ImageTagger("images/unsplash-images-collection", "image_metadata.json")
        self.w.show()
    def update_image_count(self):
        count = 0
        try:
            for _ in os.listdir("images/unsplash-images-collection"):
                count += 1
        except FileNotFoundError:
            pass
        self.image_count_label.setText(f"Nombre d'images: {count}")

    def download_images(self):
        image_folder = "images/unsplash-images-collection"
        if os.path.exists(image_folder):
            for file in os.listdir(image_folder):
                os.remove(os.path.join(image_folder, file))

        acquisition.acquire()
        self.update_image_count()

        metadata_file = "image_metadata.json"
        if os.path.exists(metadata_file):
            os.remove(metadata_file)

        metadata.create_metadata()

        QMessageBox.information(self, "Téléchargement terminé", "Les images ont été téléchargées avec succès.")

if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()