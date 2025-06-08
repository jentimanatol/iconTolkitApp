# pip install PyQt5
# pip install pillow

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                            QHBoxLayout, QFileDialog, QLabel, QWidget, QMessageBox)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from PIL import Image


class JPGtoICOConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.source_file = None
        
    def initUI(self):
        # Set window properties
        self.setWindowTitle('JPG to ICO Converter')
        self.setGeometry(300, 300, 500, 400)
        
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
        self.status_label = QLabel("Select a JPG file to convert")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        # Upload button
        self.upload_btn = QPushButton("Upload JPG")
        self.upload_btn.clicked.connect(self.upload_file)
        button_layout.addWidget(self.upload_btn)
        
        # Convert and save button
        self.save_btn = QPushButton("Convert & Save as ICO")
        self.save_btn.clicked.connect(self.save_file)
        self.save_btn.setEnabled(False)  # Disable until image is selected
        button_layout.addWidget(self.save_btn)
        
        main_layout.addLayout(button_layout)
    
    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select JPG Image", "", "JPG Files (*.jpg *.jpeg);;All Files (*)"
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
            QMessageBox.warning(self, "Warning", "Please select a JPG file first!")
            return
            
        # Set default filename to app_icon.ico
        default_dir = os.path.dirname(self.source_file)
        default_name = "app_icon.ico"
        
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save ICO File", os.path.join(default_dir, default_name), 
            "Icon Files (*.ico);;All Files (*)"
        )
        
        if save_path:
            try:
                # Convert JPG to ICO
                img = Image.open(self.source_file)
                
                # Create icon in multiple sizes for better compatibility
                sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)]
                img.save(save_path, format='ICO', sizes=sizes)
                
                self.status_label.setText(f"Successfully saved: {os.path.basename(save_path)}")
                QMessageBox.information(self, "Success", "Image successfully converted to ICO format!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


def main():
    app = QApplication(sys.argv)
    converter = JPGtoICOConverter()
    converter.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
