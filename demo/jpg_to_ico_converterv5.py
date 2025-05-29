





import sys
import os

import sys
import traceback

from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                            QHBoxLayout, QFileDialog, QLabel, QWidget, QMessageBox,
                            QComboBox, QGridLayout, QSpinBox)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from PIL import Image












class IconGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.icon_image = None
        self.icon_size = 256
        
    def initUI(self):
        main_layout = QVBoxLayout(self)
        
        # Preview
        self.preview_label = QLabel("Icon Preview")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(256)
        self.preview_label.setMinimumWidth(256)
        self.preview_label.setStyleSheet("border: 1px solid #ccc; background-color: #f0f0f0;")
        main_layout.addWidget(self.preview_label)
        
        # Controls
        controls_layout = QGridLayout()
        
        # Text input
        text_label = QLabel("Text:")
        self.text_input = QLineEdit("C++")
        controls_layout.addWidget(text_label, 0, 0)
        controls_layout.addWidget(self.text_input, 0, 1)
        
        # Font selection
        font_label = QLabel("Font:")
        self.font_selector = QFontComboBox()
        self.font_selector.setCurrentFont(QFont("Arial Black"))
        controls_layout.addWidget(font_label, 1, 0)
        controls_layout.addWidget(self.font_selector, 1, 1)
        
        # Font size
        font_size_label = QLabel("Font Size:")
        self.font_size_slider = QSlider(Qt.Horizontal)
        self.font_size_slider.setMinimum(10)
        self.font_size_slider.setMaximum(100)
        self.font_size_slider.setValue(60)
        controls_layout.addWidget(font_size_label, 2, 0)
        controls_layout.addWidget(self.font_size_slider, 2, 1)
        
        # Base color
        base_color_label = QLabel("Base Color:")
        self.base_color_btn = QPushButton()
        self.base_color_btn.setStyleSheet("background-color: #4B8BBE;")
        self.base_color = QColor(75, 139, 190)  # A nice blue color
        self.base_color_btn.clicked.connect(self.select_base_color)
        controls_layout.addWidget(base_color_label, 3, 0)
        controls_layout.addWidget(self.base_color_btn, 3, 1)
        
        # Text color
        text_color_label = QLabel("Text Color:")
        self.text_color_btn = QPushButton()
        self.text_color_btn.setStyleSheet("background-color: #FFFFFF;")
        self.text_color = QColor(255, 255, 255)  # White
        self.text_color_btn.clicked.connect(self.select_text_color)
        controls_layout.addWidget(text_color_label, 4, 0)
        controls_layout.addWidget(self.text_color_btn, 4, 1)
        
        # 3D effect depth
        depth_label = QLabel("3D Effect Depth:")
        self.depth_slider = QSlider(Qt.Horizontal)
        self.depth_slider.setMinimum(5)
        self.depth_slider.setMaximum(50)
        self.depth_slider.setValue(20)
        controls_layout.addWidget(depth_label, 5, 0)
        controls_layout.addWidget(self.depth_slider, 5, 1)
        
        # Generate button
        self.generate_btn = QPushButton("Generate Icon")
        self.generate_btn.clicked.connect(self.generate_icon)
        controls_layout.addWidget(self.generate_btn, 6, 0, 1, 2)
        
        # Save button
        self.save_btn = QPushButton("Save Icon")
        self.save_btn.clicked.connect(self.save_icon)
        self.save_btn.setEnabled(False)
        controls_layout.addWidget(self.save_btn, 7, 0, 1, 2)
        
        # Connect changes to preview update
        self.text_input.textChanged.connect(lambda: self.generate_icon())
        self.font_selector.currentFontChanged.connect(lambda: self.generate_icon())
        self.font_size_slider.valueChanged.connect(lambda: self.generate_icon())
        self.depth_slider.valueChanged.connect(lambda: self.generate_icon())
        
        main_layout.addLayout(controls_layout)
        
        # Generate initial preview
        self.generate_icon()
        
    def select_base_color(self):
        color = QColorDialog.getColor(self.base_color, self, "Select Base Color")
        if color.isValid():
            self.base_color = color
            self.base_color_btn.setStyleSheet(f"background-color: {color.name()};")
            self.generate_icon()
    
    def select_text_color(self):
        color = QColorDialog.getColor(self.text_color, self, "Select Text Color")
        if color.isValid():
            self.text_color = color
            self.text_color_btn.setStyleSheet(f"background-color: {color.name()};")
            self.generate_icon()
    
    def generate_icon(self):
        try:
            size = self.icon_size
            text = self.text_input.text() or "C++"
            font_name = self.font_selector.currentFont().family()
            font_size = self.font_size_slider.value()
            depth = self.depth_slider.value()
            
            # Create a high-resolution image for better quality
            img_size = size * 4
            
            # Create base image with PIL
            img = Image.new('RGBA', (img_size, img_size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Define colors
            base_color = (self.base_color.red(), self.base_color.green(), self.base_color.blue())
            text_color = (self.text_color.red(), self.text_color.green(), self.text_color.blue())
            
            # Create a folder-like shape with 3D effect
            # Draw the base folder icon
            padding = img_size // 10
            folder_width = img_size - 2 * padding
            folder_height = int(folder_width * 0.85)
            
            # Calculate 3D effect coordinates
            offset_3d = depth * 4  # Scale depth for high-res
            
            # Draw the shadow part first (3D effect)
            shadow_points = [
                (padding + offset_3d, padding + offset_3d),  # top-left
                (padding + folder_width, padding + offset_3d),  # top-right
                (padding + folder_width, padding + folder_height),  # bottom-right
                (padding, padding + folder_height),  # bottom-left
            ]
            
            # Draw a darker shadow
            shadow_color = tuple(max(0, c - 80) for c in base_color) + (200,)  # Darker with some transparency
            draw.polygon(shadow_points, fill=shadow_color)
            
            # Draw the main folder
            folder_points = [
                (padding, padding),  # top-left
                (padding + folder_width - offset_3d, padding),  # top-right
                (padding + folder_width - offset_3d, padding + folder_height - offset_3d),  # bottom-right
                (padding, padding + folder_height - offset_3d),  # bottom-left
            ]
            draw.polygon(folder_points, fill=base_color)
            
            # Draw the tab part of folder
            tab_height = img_size // 8
            tab_width = folder_width // 3
            
            # 3D effect for tab
            tab_shadow_points = [
                (padding + offset_3d, padding + offset_3d),
                (padding + tab_width + offset_3d, padding + offset_3d),
                (padding + tab_width + offset_3d, padding - tab_height + offset_3d),
                (padding + offset_3d, padding - tab_height + offset_3d),
            ]
            draw.polygon(tab_shadow_points, fill=shadow_color)
            
            # Main tab
            tab_points = [
                (padding, padding),
                (padding + tab_width, padding),
                (padding + tab_width, padding - tab_height),
                (padding, padding - tab_height),
            ]
            draw.polygon(tab_points, fill=base_color)
            
            # Add highlights for 3D glossy effect
            highlight_color = tuple(min(255, c + 70) for c in base_color) + (150,)
            
            # Diagonal glossy highlight
            highlight_points = [
                (padding, padding),
                (padding + folder_width // 3, padding),
                (padding, padding + folder_height // 3),
            ]
            draw.polygon(highlight_points, fill=highlight_color)
            
            # Try to load font, use default if not available
            try:
                font = ImageFont.truetype(font_name, font_size * 4)  # Scale for high-res
            except IOError:
                font = ImageFont.load_default()
            
            # Calculate text position to center it
            # Newer Pillow versions use different methods for text size
            try:
                # For newer Pillow versions
                left, top, right, bottom = font.getbbox(text)
                text_width = right - left
                text_height = bottom - top
            except AttributeError:
                try:
                    # Alternative method
                    text_width, text_height = font.getsize(text)
                except:
                    # Fallback for even older versions
                    text_width = img_size // 2
                    text_height = img_size // 6
            
            text_x = (img_size - text_width) // 2
            text_y = (img_size - text_height) // 2
            
            # Draw text shadow for 3D effect
            shadow_offset = depth // 2
            draw.text((text_x + shadow_offset, text_y + shadow_offset), text, 
                    fill=(0, 0, 0, 180), font=font)
            
            # Draw main text
            draw.text((text_x, text_y), text, fill=text_color, font=font)
            
            # Apply a slight blur for softer edges
            img = img.filter(ImageFilter.GaussianBlur(radius=1))
            
            # Resize to target size with high quality
            img = img.resize((size, size), Image.LANCZOS)
            
            # Store the generated icon
            self.icon_image = img
            self.save_btn.setEnabled(True)
            
            # Update preview
            img_qt = self.pil_to_pixmap(img)
            self.preview_label.setPixmap(img_qt)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not generate icon: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def pil_to_pixmap(self, pil_image):
        # Convert PIL image to QPixmap for display
        if pil_image.mode != "RGBA":
            pil_image = pil_image.convert("RGBA")
        
        data = pil_image.tobytes("raw", "RGBA")
        qim = QPixmap.fromImage(
            QPixmap.fromImage(QPixmap.fromImage(QImage(
                data, pil_image.width, pil_image.height, QImage.Format_RGBA8888
            )))
        )
        return qim
    
    def save_icon(self):
        if not self.icon_image:
            QMessageBox.warning(self, "Warning", "Please generate an icon first!")
            return
        
        default_name = "app_icon.ico"
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save ICO File", default_name, 
            "Icon Files (*.ico);;All Files (*)"
        )
        
        if save_path:
            try:
                # Create icon in multiple sizes for better compatibility
                sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
                self.icon_image.save(save_path, format='ICO', sizes=sizes)
                
                QMessageBox.information(self, "Success", "Icon successfully saved!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
                import traceback
                traceback.print_exc()import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                            QHBoxLayout, QFileDialog, QLabel, QWidget, QMessageBox,
                            QComboBox, QGridLayout, QSpinBox, QTabWidget, QColorDialog,
                            QLineEdit, QFontComboBox, QSlider)
from PyQt5.QtGui import QIcon, QPixmap, QColor, QPainter, QLinearGradient, QFont, QFontMetrics, QPen, QRadialGradient, QImage
from PyQt5.QtCore import Qt, QRect, QPoint, QSize
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageEnhance


class ImageToICOConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.source_file = None
        self.icon_size = 256  # Default size
        
    def initUI(self):
        # Set window properties
        self.setWindowTitle('Image to ICO Converter')
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
        sizes = ["16×16", "24×24", "32×32", "48×48", "64×64", "128×128", "256×256"]
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
            
        # Set default filename to app_icon.ico
        default_dir = os.path.dirname(self.source_file)
        default_name = "app_icon.ico"
        
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
                for size in [16, 24, 32, 48, 64, 128, 256]:
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


class ImageToICOApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Set window properties
        self.setWindowTitle('Image to ICO Converter & Generator')
        self.setGeometry(300, 300, 800, 600)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Create tabs
        self.converter_tab = ImageToICOConverter()
        self.generator_tab = IconGenerator()
        
        # Add tabs
        self.tabs.addTab(self.converter_tab, "Image Converter")
        self.tabs.addTab(self.generator_tab, "C++ Icon Generator")


def main():
    app = QApplication(sys.argv)
    window = ImageToICOApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
