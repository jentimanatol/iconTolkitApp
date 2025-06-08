import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image
import os

class IconApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To ICO 256x256")
        self.file = None
        layout = QVBoxLayout()
        self.label = QLabel("No image"); self.label.setAlignment(Qt.AlignCenter); layout.addWidget(self.label)
        for text, func in [("Upload PNG/JPG", self.load), ("Convert to ICO", self.convert)]:
            b = QPushButton(text); b.clicked.connect(func); layout.addWidget(b)
        w = QWidget(); w.setLayout(layout); self.setCentralWidget(w)

    def load(self):
        f, _ = QFileDialog.getOpenFileName(self, "Open", "", "Images (*.png *.jpg *.jpeg)")
        if f: self.file = f; self.label.setPixmap(QPixmap(f).scaled(200,200, Qt.KeepAspectRatio))

    def convert(self):
        if not self.file: return
        out, _ = QFileDialog.getSaveFileName(self, "Save ICO", os.path.join(os.path.dirname(self.file), "icon.ico"), "ICO Files (*.ico)")
        if out: Image.open(self.file).convert("RGBA").resize((256,256)).save(out, format="ICO")

app = QApplication(sys.argv)
win = IconApp(); win.show()
sys.exit(app.exec_())
