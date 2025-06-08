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
        # Set window properties - bigger and more modern
        self.setWindowTitle('🎨 Icon Maker by AJ - Professional Icon Converter')
        self.setGeometry(200, 100, 900, 750)
        self.setMinimumSize(800, 650)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Set main window style
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
            QWidget {
                background: transparent;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        # Title label
        title_label = QLabel("🎨 Professional Icon Converter")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: white;
                margin: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
        """)
        main_layout.addWidget(title_label)
        
        # Image preview container
        preview_container = QWidget()
        preview_container.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                border: 3px solid rgba(255, 255, 255, 0.3);
            }
        """)
        preview_layout = QVBoxLayout(preview_container)
        preview_layout.setContentsMargins(20, 20, 20, 20)
        
        # Image preview label
        self.preview_label = QLabel("📸 Drop your image here or click Upload!")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(300)
        self.preview_label.setStyleSheet("""
            QLabel {
                border: 3px dashed #4CAF50;
                border-radius: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8f9ff, stop:1 #e8f5e8);
                font-size: 18px;
                color: #2E7D32;
                font-weight: bold;
                padding: 20px;
            }
        """)
        preview_layout.addWidget(self.preview_label)
        main_layout.addWidget(preview_container)
        
        # Status label
        self.status_label = QLabel("✨ Ready to create amazing icons!")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: white;
                font-weight: bold;
                padding: 10px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 15px;
                margin: 5px;
            }
        """)
        main_layout.addWidget(self.status_label)
        
        # Settings container
        settings_container = QWidget()
        settings_container.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.9);
                border-radius: 15px;
                border: 2px solid rgba(255, 255, 255, 0.3);
            }
        """)
        settings_layout = QHBoxLayout(settings_container)
        settings_layout.setContentsMargins(25, 20, 25, 20)
        
        # Size options
        size_label = QLabel("🎯 Icon Size:")
        size_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2E7D32;
                margin-right: 10px;
            }
        """)
        
        self.size_selector = QComboBox()
        sizes = ["16×16", "24×24", "32×32", "48×48", "64×64", "128×128", "256×256", "512×512"]
        self.size_selector.addItems(sizes)
        self.size_selector.setCurrentIndex(6)  # Default to 256x256
        self.size_selector.currentIndexChanged.connect(self.update_size)
        self.size_selector.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                padding: 8px 15px;
                border: 2px solid #4CAF50;
                border-radius: 10px;
                background: white;
                color: #2E7D32;
                font-weight: bold;
                min-width: 120px;
            }
            QComboBox::drop-down {
                border: none;
                background: #4CAF50;
                border-radius: 5px;
                margin: 2px;
            }
            QComboBox::down-arrow {
                image: none;
                border: 5px solid transparent;
                border-top: 8px solid white;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #4CAF50;
                border-radius: 10px;
                background: white;
                selection-background-color: #E8F5E8;
                color: #2E7D32;
            }
        """)
        
        settings_layout.addWidget(size_label)
        settings_layout.addWidget(self.size_selector)
        settings_layout.addStretch()
        
        main_layout.addWidget(settings_container)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        
        # Upload button
        self.upload_btn = QPushButton("📁 Upload Image")
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                padding: 15px 30px;
                border: none;
                border-radius: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FF6B6B, stop:1 #FF8E53);
                color: white;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FF8E53, stop:1 #FF6B6B);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #E55A5A, stop:1 #E57C42);
            }
        """)
        button_layout.addWidget(self.upload_btn)
        
        # Convert and save button
        self.save_btn = QPushButton("💾 Convert & Save as ICO")
        self.save_btn.clicked.connect(self.save_file)
        self.save_btn.setEnabled(False)  # Disable until image is selected
        self.save_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                padding: 15px 30px;
                border: none;
                border-radius: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4CAF50, stop:1 #45a049);
                color: white;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            }
            QPushButton:hover:enabled {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #45a049, stop:1 #4CAF50);
                transform: translateY(-2px);
            }
            QPushButton:pressed:enabled {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3d8b40, stop:1 #3a7f3d);
            }
            QPushButton:disabled {
                background: #cccccc;
                color: #666666;
            }
        """)
        button_layout.addWidget(self.save_btn)
        
        main_layout.addLayout(button_layout)
    
    def update_size(self, index):
        size_text = self.size_selector.currentText()
        self.icon_size = int(size_text.split("×")[0])
    
    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "🎨 Select Your Amazing Image", "", 
            "Image Files (*.jpg *.jpeg *.png *.webp *.bmp *.gif);;All Files (*)"
        )
        
        if file_path:
            self.source_file = file_path
            self.status_label.setText(f"🎉 Selected: {os.path.basename(file_path)} - Ready to convert!")
            self.save_btn.setEnabled(True)
            
            # Display preview with better styling
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(280, 280, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.preview_label.setPixmap(pixmap)
                self.preview_label.setAlignment(Qt.AlignCenter)
                self.preview_label.setStyleSheet("""
                    QLabel {
                        border: 3px solid #4CAF50;
                        border-radius: 15px;
                        background: white;
                        padding: 10px;
                    }
                """)
            else:
                self.preview_label.setText("❌ Cannot display preview")
                self.preview_label.setStyleSheet("""
                    QLabel {
                        border: 3px dashed #FF6B6B;
                        border-radius: 15px;
                        background: #ffebee;
                        font-size: 16px;
                        color: #c62828;
                        font-weight: bold;
                        padding: 20px;
                    }
                """)
    
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
                
                self.status_label.setText(f"✅ Successfully saved: {os.path.basename(save_path)}")
                QMessageBox.information(self, "🎉 Success!", 
                                        f"🎨 Image successfully converted to ICO format!\n\n"
                                        f"📊 Created with {len(sizes)} size variants:\n"
                                        f"📁 Saved as: {os.path.basename(save_path)}")
            except Exception as e:
                self.status_label.setText("❌ Error occurred during conversion")
                QMessageBox.critical(self, "❌ Error", f"An error occurred:\n\n{str(e)}")
                import traceback
                traceback.print_exc()


def main():
    app = QApplication(sys.argv)
    converter = Ico_maker()
    converter.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()