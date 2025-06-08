import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                            QHBoxLayout, QFileDialog, QLabel, QWidget, QMessageBox,
                            QComboBox, QGridLayout, QSpinBox)
from PyQt5.QtGui import QIcon, QPixmap, QDragEnterEvent, QDropEvent
from PyQt5.QtCore import Qt, QUrl
from PIL import Image


class DropLabel(QLabel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and self.is_image_file(urls[0].toLocalFile()):
                event.accept()
                self.setStyleSheet("""
                    QLabel {
                        border: 3px dashed #ff1493;
                        border-radius: 20px;
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                            stop:0 rgba(255, 20, 147, 0.3),
                            stop:0.5 rgba(255, 107, 53, 0.3),
                            stop:1 rgba(255, 215, 0, 0.3));
                        font-size: 22px;
                        color: #ff1493;
                        font-weight: 900;
                        padding: 30px;
                        text-shadow: 
                            0px 0px 15px rgba(255, 20, 147, 0.9),
                            2px 2px 6px rgba(0, 0, 0, 0.8);
                        letter-spacing: 3px;
                        box-shadow: 
                            inset 0 0 30px rgba(255, 20, 147, 0.4),
                            0 0 30px rgba(255, 20, 147, 0.5);
                    }
                """)
                self.setText("♦ DROP TO FORGE ♦")
            else:
                event.ignore()
        else:
            event.ignore()
    
    def dragLeaveEvent(self, event):
        self.setStyleSheet("""
            QLabel {
                border: 3px dashed #00f5ff;
                border-radius: 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0, 245, 255, 0.1),
                    stop:0.5 rgba(138, 43, 226, 0.1),
                    stop:1 rgba(255, 20, 147, 0.1));
                font-size: 20px;
                color: #00f5ff;
                font-weight: 800;
                padding: 30px;
                text-shadow: 
                    0px 0px 10px rgba(0, 245, 255, 0.8),
                    2px 2px 4px rgba(0, 0, 0, 0.5);
                letter-spacing: 3px;
                box-shadow: 
                    inset 0 0 20px rgba(0, 245, 255, 0.2),
                    0 0 20px rgba(0, 245, 255, 0.3);
            }
        """)
        if not self.pixmap():
            self.setText("▼ DRAG IMAGE HERE ▼")
    
    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if self.is_image_file(file_path):
                self.parent.load_image(file_path)
                event.accept()
            else:
                event.ignore()
                QMessageBox.warning(self.parent, "⚠ INVALID FORMAT", 
                                  "◆ UNSUPPORTED FILE TYPE ◆\n\n"
                                  "▸ ACCEPTED: JPG, PNG, WEBP, BMP, GIF\n"
                                  "▸ STATUS: REJECTEDDrop your image here or click Upload!")
    
    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if self.is_image_file(file_path):
                self.parent.load_image(file_path)
                event.accept()
            else:
                event.ignore()
                QMessageBox.warning(self.parent, "❌ Invalid File", 
                                  "Please drop a valid image file!\n\n"
                                  "Supported formats: JPG, PNG, WEBP, BMP, GIF")
    
    def is_image_file(self, file_path):
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif']
        return any(file_path.lower().endswith(ext) for ext in valid_extensions)


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
        
        # Set main window style with 3D effects
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e, stop:0.3 #16213e, stop:0.7 #0f3460, stop:1 #533483);
            }
            QWidget {
                background: transparent;
                font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
            }
        """)
        
        # Title label with 3D effect
        title_label = QLabel("⚡ ICON FORGE STUDIO ⚡")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: 900;
                color: #00f5ff;
                margin: 15px;
                text-shadow: 
                    0px 0px 20px rgba(0, 245, 255, 0.8),
                    0px 0px 40px rgba(0, 245, 255, 0.6),
                    3px 3px 0px #1a1a2e,
                    6px 6px 0px rgba(0, 0, 0, 0.3);
                letter-spacing: 2px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0, 245, 255, 0.1), 
                    stop:0.5 rgba(138, 43, 226, 0.1), 
                    stop:1 rgba(255, 20, 147, 0.1));
                border-radius: 20px;
                padding: 20px;
                border: 2px solid rgba(0, 245, 255, 0.3);
            }
        """)
        main_layout.addWidget(title_label)
        
        # Image preview container with glassmorphism
        preview_container = QWidget()
        preview_container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.15),
                    stop:0.5 rgba(255, 255, 255, 0.1),
                    stop:1 rgba(255, 255, 255, 0.05));
                border-radius: 25px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                backdrop-filter: blur(20px);
                box-shadow: 
                    0 8px 32px rgba(0, 0, 0, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
            }
        """)
        preview_layout = QVBoxLayout(preview_container)
        preview_layout.setContentsMargins(25, 25, 25, 25)
        
        # Image preview label with 3D drop zone
        self.preview_label = DropLabel(self)
        self.preview_label.setText("▼ DRAG IMAGE HERE ▼")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(300)
        self.preview_label.setStyleSheet("""
            QLabel {
                border: 3px dashed #00f5ff;
                border-radius: 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0, 245, 255, 0.1),
                    stop:0.5 rgba(138, 43, 226, 0.1),
                    stop:1 rgba(255, 20, 147, 0.1));
                font-size: 20px;
                color: #00f5ff;
                font-weight: 800;
                padding: 30px;
                text-shadow: 
                    0px 0px 10px rgba(0, 245, 255, 0.8),
                    2px 2px 4px rgba(0, 0, 0, 0.5);
                letter-spacing: 3px;
                box-shadow: 
                    inset 0 0 20px rgba(0, 245, 255, 0.2),
                    0 0 20px rgba(0, 245, 255, 0.3);
            }
        """)
        preview_layout.addWidget(self.preview_label)
        main_layout.addWidget(preview_container)
        
        # Status label with neon effect
        self.status_label = QLabel("◆ READY TO FORGE ICONS ◆")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #ff1493;
                font-weight: 700;
                padding: 15px 25px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 20, 147, 0.2),
                    stop:0.5 rgba(138, 43, 226, 0.2),
                    stop:1 rgba(0, 245, 255, 0.2));
                border-radius: 20px;
                border: 1px solid rgba(255, 20, 147, 0.5);
                margin: 10px;
                text-shadow: 
                    0px 0px 15px rgba(255, 20, 147, 0.8),
                    2px 2px 4px rgba(0, 0, 0, 0.5);
                letter-spacing: 1px;
                box-shadow: 
                    0 0 20px rgba(255, 20, 147, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
            }
        """)
        main_layout.addWidget(self.status_label)
        
        # Settings container with 3D depth
        settings_container = QWidget()
        settings_container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.12),
                    stop:1 rgba(255, 255, 255, 0.08));
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.15);
                box-shadow: 
                    0 8px 32px rgba(0, 0, 0, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.15);
            }
        """)
        settings_layout = QHBoxLayout(settings_container)
        settings_layout.setContentsMargins(30, 25, 30, 25)
        
        # Size options with futuristic style
        size_label = QLabel("◈ SIZE MATRIX")
        size_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 800;
                color: #00f5ff;
                margin-right: 15px;
                text-shadow: 
                    0px 0px 10px rgba(0, 245, 255, 0.8),
                    2px 2px 4px rgba(0, 0, 0, 0.5);
                letter-spacing: 1px;
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
                font-weight: 700;
                padding: 12px 20px;
                border: 2px solid #00f5ff;
                border-radius: 15px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 0, 0, 0.3),
                    stop:1 rgba(0, 0, 0, 0.1));
                color: #00f5ff;
                min-width: 140px;
                text-shadow: 0px 0px 8px rgba(0, 245, 255, 0.6);
                box-shadow: 
                    0 0 15px rgba(0, 245, 255, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
            }
            QComboBox::drop-down {
                border: none;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00f5ff, stop:1 #008b8b);
                border-radius: 8px;
                margin: 3px;
                box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.3);
            }
            QComboBox::down-arrow {
                image: none;
                border: 6px solid transparent;
                border-top: 10px solid #1a1a2e;
                margin-right: 8px;
            }
            QComboBox:hover {
                box-shadow: 
                    0 0 25px rgba(0, 245, 255, 0.5),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
            }
            QComboBox QAbstractItemView {
                border: 2px solid #00f5ff;
                border-radius: 15px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a1a2e, stop:1 #0f3460);
                selection-background-color: rgba(0, 245, 255, 0.3);
                color: #00f5ff;
                font-weight: 700;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            }
        """)
        
        settings_layout.addWidget(size_label)
        settings_layout.addWidget(self.size_selector)
        settings_layout.addStretch()
        
        main_layout.addWidget(settings_container)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        
        # Upload button with 3D cyberpunk style
        self.upload_btn = QPushButton("▲ UPLOAD IMAGE")
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: 800;
                padding: 18px 35px;
                border: none;
                border-radius: 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ff6b35, stop:0.5 #f7931e, stop:1 #ff4757);
                color: white;
                text-shadow: 
                    0px 0px 10px rgba(255, 107, 53, 0.8),
                    2px 2px 4px rgba(0, 0, 0, 0.6);
                letter-spacing: 2px;
                box-shadow: 
                    0 8px 25px rgba(255, 107, 53, 0.4),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2),
                    inset 0 -1px 0 rgba(0, 0, 0, 0.2);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ff8b55, stop:0.5 #ffb33e, stop:1 #ff6777);
                box-shadow: 
                    0 12px 35px rgba(255, 107, 53, 0.6),
                    inset 0 1px 0 rgba(255, 255, 255, 0.3);
                transform: translateY(-3px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e55a32, stop:0.5 #e6821b, stop:1 #e63946);
                transform: translateY(1px);
                box-shadow: 
                    0 4px 15px rgba(255, 107, 53, 0.3),
                    inset 0 -2px 0 rgba(0, 0, 0, 0.3);
            }
        """)
        button_layout.addWidget(self.upload_btn)
        
        # Convert and save button with holographic effect
        self.save_btn = QPushButton("◆ FORGE ICO FILE")
        self.save_btn.clicked.connect(self.save_file)
        self.save_btn.setEnabled(False)  # Disable until image is selected
        self.save_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: 800;
                padding: 18px 35px;
                border: none;
                border-radius: 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00f5ff, stop:0.5 #8a2be2, stop:1 #ff1493);
                color: white;
                text-shadow: 
                    0px 0px 15px rgba(0, 245, 255, 0.8),
                    2px 2px 4px rgba(0, 0, 0, 0.6);
                letter-spacing: 2px;
                box-shadow: 
                    0 8px 25px rgba(0, 245, 255, 0.4),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2),
                    inset 0 -1px 0 rgba(0, 0, 0, 0.2);
            }
            QPushButton:hover:enabled {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #20f5ff, stop:0.5 #aa4bf2, stop:1 #ff34a3);
                box-shadow: 
                    0 12px 35px rgba(0, 245, 255, 0.6),
                    inset 0 1px 0 rgba(255, 255, 255, 0.3);
                transform: translateY(-3px);
            }
            QPushButton:pressed:enabled {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d4e6, stop:0.5 #7a23c8, stop:1 #e61279);
                transform: translateY(1px);
                box-shadow: 
                    0 4px 15px rgba(0, 245, 255, 0.3),
                    inset 0 -2px 0 rgba(0, 0, 0, 0.3);
            }
            QPushButton:disabled {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #666666, stop:1 #444444);
                color: #999999;
                box-shadow: none;
                text-shadow: none;
            }
        """)
        button_layout.addWidget(self.save_btn)
        
        main_layout.addLayout(button_layout)
    
    def update_size(self, index):
        size_text = self.size_selector.currentText()
        self.icon_size = int(size_text.split("×")[0])
    
    def load_image(self, file_path):
        """Load image from file path (used by both upload button and drag&drop)"""
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
    
    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "🎨 Select Your Amazing Image", "", 
            "Image Files (*.jpg *.jpeg *.png *.webp *.bmp *.gif);;All Files (*)"
        )
        
        if file_path:
            self.load_image(file_path)
    
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