from pathlib import Path
import json
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap


class ImageTagger(QWidget):
    def __init__(self, image_folder, metadata_file):
        super().__init__()
        self.tag_entry = None
        self.img_label = None
        self.image_folder = Path(image_folder)
        self.metadata_file = Path(metadata_file)
        self.image_files = self.get_image_files()
        self.metadata = self.load_metadata()
        self.current_image_index = 0
        self.setWindowTitle("Image Tagger")
        self.create_widgets()
        self.update_image()

    def get_image_files(self):
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif')
        return [file.name for file in self.image_folder.iterdir() if file.suffix.lower() in image_extensions]

    def load_metadata(self):
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        else:
            return []

    def save_metadata(self):
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=4)

    def create_widgets(self):
        main_layout = QVBoxLayout()

        self.img_label = QLabel()
        main_layout.addWidget(self.img_label)

        tag_layout = QHBoxLayout()
        self.tag_entry = QLineEdit()
        tag_layout.addWidget(self.tag_entry)

        save_button = QPushButton("Save Tag")
        save_button.clicked.connect(self.save_tag)
        tag_layout.addWidget(save_button)

        main_layout.addLayout(tag_layout)

        button_layout = QHBoxLayout()
        prev_button = QPushButton("Previous Image")
        prev_button.clicked.connect(self.prev_image)
        button_layout.addWidget(prev_button)

        next_button = QPushButton("Next Image")
        next_button.clicked.connect(self.next_image)
        button_layout.addWidget(next_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def update_image(self):
        image_path = self.image_folder / self.image_files[self.current_image_index]
        pixmap = QPixmap(str(image_path))
        self.img_label.setPixmap(pixmap)

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
                    entry["tags"].append(tag)
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
