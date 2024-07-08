import sys
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget, QApplication
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image
from image_operations import *

class ImageApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image App")
        self.setMinimumSize(800, 600)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        self.upload_button = QPushButton("Загрузить изображение")
        self.camera_button = QPushButton("Подключить вебкамеру")
        self.negative_button = QPushButton("Показать негативное изображение")
        self.average_button = QPushButton("Усреднить изображение")
        self.rectangle_button = QPushButton("Нарисовать прямоугольник")
        self.red_channel_button = QPushButton("Показать красный канал")
        self.green_channel_button = QPushButton("Показать зеленый канал")
        self.blue_channel_button = QPushButton("Показать синий канал")

        self.setup_layout()

        self.image = None
        self.original_image = None
        self.channel_displayed = None

    def setup_layout(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.image_label)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.camera_button)
        layout.addWidget(self.negative_button)
        layout.addWidget(self.average_button)
        layout.addWidget(self.rectangle_button)
        layout.addWidget(self.red_channel_button)
        layout.addWidget(self.green_channel_button)
        layout.addWidget(self.blue_channel_button)
        self.setCentralWidget(central_widget)

        self.upload_button.clicked.connect(self.upload_image)
        self.camera_button.clicked.connect(lambda: capture_from_webcam(self))  # Изменили вызов метода
        self.negative_button.clicked.connect(lambda: show_negative(self))  # Изменили вызов метода
        self.average_button.clicked.connect(lambda: average_image(self))  # Изменили вызов метода
        self.rectangle_button.clicked.connect(lambda: draw_rectangle(self))  # Изменили вызов метода
        self.red_channel_button.clicked.connect(lambda: show_color_channel(self, 'red'))  # Изменили вызов метода
        self.green_channel_button.clicked.connect(lambda: show_color_channel(self, 'green'))  # Изменили вызов метода
        self.blue_channel_button.clicked.connect(lambda: show_color_channel(self, 'blue'))  # Изменили вызов метода

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image files (*.jpg *.png)")
        if file_path:
            self.image = Image.open(file_path)
            self.original_image = self.image.copy()
            self.display_image(self.image)

    def display_image(self, image):
        qimage = QImage(image.tobytes(), image.width, image.height, image.width * 3, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageApp()
    window.show()
    sys.exit(app.exec_())
