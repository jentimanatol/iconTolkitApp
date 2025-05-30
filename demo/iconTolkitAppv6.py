import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                            QHBoxLayout, QFileDialog, QLabel, QWidget, QMessageBox,
                            QComboBox, QGridLayout, QSpinBox)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from PIL import Image


class Ico_maker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.source_file = None
        self.icon_size = 256  # Default size
        
    def initUI(self):
        # Set window properties
        self.setWindowTitle('Icon Maker by AJ')
        self.setGeometry(300, 300, 600, 500)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Image preview label
        self.preview_label = QLabel("No image selected")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(200)
        self.preview_label.setStyleSheet("border: 1px solid #ccc; background-color: #f0f0f0;")
        main_layout.addWidget(self.preview_label)
        
        # Status label
        self.status_label = QLabel("Select an image file to convert")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # Settings grid
        settings_layout = QGridLayout()
        
        # Size options
        size_label = QLabel("Icon Size:")
        self.size_selector = QComboBox()
        sizes = ["16×16", "24×24", "32×32", "48×48", "64×64", "128×128", "256×256", "512×512"]
        self.size_selector.addItems(sizes)
        self.size_selector.setCurrentIndex(6)  # Default to 256x256
        self.size_selector.currentIndexChanged.connect(self.update_size)
        
        settings_layout.addWidget(size_label, 0, 0)
        settings_layout.addWidget(self.size_selector, 0, 1)
        
        main_layout.addLayout(settings_layout)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        # Upload button
        self.upload_btn = QPushButton("Upload Image")
        self.upload_btn.clicked.connect(self.upload_file)
        button_layout.addWidget(self.upload_btn)
        
        # Convert and save button
        self.save_btn = QPushButton("Convert & Save as ICO")
        self.save_btn.clicked.connect(self.save_file)
        self.save_btn.setEnabled(False)  # Disable until image is selected
        button_layout.addWidget(self.save_btn)
        
        main_layout.addLayout(button_layout)
    
    def update_size(self, index):
        size_text = self.size_selector.currentText()
        self.icon_size = int(size_text.split("×")[0])
    
    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", 
            "Image Files (*.jpg *.jpeg *.png *.webp);;All Files (*)"
        )
        
        if file_path:
            self.source_file = file_path
            self.status_label.setText(f"Selected: {os.path.basename(file_path)}")
            self.save_btn.setEnabled(True)
            
            # Display preview
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.preview_label.setPixmap(pixmap)
                self.preview_label.setAlignment(Qt.AlignCenter)
            else:
                self.preview_label.setText("Cannot display preview")
    
    def save_file(self):
        if not self.source_file:
            QMessageBox.warning(self, "Warning", "Please select an image file first!")
            return
            
        # Get the current selected size for the filename
        current_size = self.size_selector.currentText()
        
        # Set default filename to include the selected size
        default_dir = os.path.dirname(self.source_file)
        default_name = f"app_icon_{current_size}.ico"
        
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save ICO File", os.path.join(default_dir, default_name), 
            "Icon Files (*.ico);;All Files (*)"
        )
        
        if save_path:
            try:
                # Create ICO file using PIL
                img = Image.open(self.source_file)
                
                # Ensure RGBA mode for transparency support
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # Calculate sizes to include
                base_size = self.icon_size
                sizes = []
                for size in [16, 24, 32, 48, 64, 128, 256, 512]:
                    if size <= base_size:
                        sizes.append((size, size))
                
                # Create a new image with transparency
                icon_image = img.copy()
                
                # Resize to the largest requested size if needed
                if max(icon_image.size) > base_size:
                    # Maintain aspect ratio
                    if icon_image.width > icon_image.height:
                        new_width = base_size
                        new_height = int(icon_image.height * (base_size / icon_image.width))
                    else:
                        new_height = base_size
                        new_width = int(icon_image.width * (base_size / icon_image.height))
                    
                    icon_image = icon_image.resize((new_width, new_height), Image.LANCZOS)
                
                # Save as ICO
                icon_image.save(save_path, format='ICO', sizes=sizes)
                
                self.status_label.setText(f"Successfully saved: {os.path.basename(save_path)}")
                QMessageBox.information(self, "Success", 
                                        f"Image successfully converted to ICO format with {len(sizes)} size variants!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
                import traceback
                traceback.print_exc()


def main():
    app = QApplication(sys.argv)
    converter = Ico_maker()
    converter.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()