import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget, \
    QInputDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image, ImageOps
import cv2
import numpy as np


class ImageApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image App")
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(800, 600)

        self.upload_button = QPushButton("Загрузить изображение")
        self.upload_button.clicked.connect(self.upload_image)

        self.camera_button = QPushButton("Подключить вебкамеру")
        self.camera_button.clicked.connect(self.capture_from_webcam)

        self.negative_button = QPushButton("Показать негативное изображение")
        self.negative_button.clicked.connect(self.show_negative)

        self.average_button = QPushButton("Усреднить изображение")
        self.average_button.clicked.connect(self.average_image)

        self.rectangle_button = QPushButton("Нарисовать прямоугольник")
        self.rectangle_button.clicked.connect(self.draw_rectangle)

        self.red_channel_button = QPushButton("Показать красный канал")
        self.red_channel_button.clicked.connect(lambda: self.show_color_channel('red'))

        self.green_channel_button = QPushButton("Показать зеленый канал")
        self.green_channel_button.clicked.connect(lambda: self.show_color_channel('green'))

        self.blue_channel_button = QPushButton("Показать синий канал")
        self.blue_channel_button.clicked.connect(lambda: self.show_color_channel('blue'))

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.camera_button)
        layout.addWidget(self.negative_button)
        layout.addWidget(self.average_button)
        layout.addWidget(self.rectangle_button)
        layout.addWidget(self.red_channel_button)
        layout.addWidget(self.green_channel_button)
        layout.addWidget(self.blue_channel_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.image = None
        self.original_image = None
        self.channel_displayed = None

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image files (*.jpg *.png)")
        if file_path:
            self.image = Image.open(file_path)
            self.original_image = self.image.copy()
            self.display_image(self.image)

    def capture_from_webcam(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Failed to connect to the webcam")
            return

        ret, frame = cap.read()
        cap.release()
        if not ret:
            print("Error: Failed to capture image")
            return

        self.image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        self.original_image = self.image.copy()
        self.display_image(self.image)

    def display_image(self, image):
        image = image.convert("RGB")
        qimage = QImage(image.tobytes(), image.width, image.height, image.width * 3, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def show_negative(self):
        if self.image is None:
            print("Error: No image loaded")
            return
        negative_image = ImageOps.invert(self.image.convert("RGB"))
        self.display_image(negative_image)
        self.image = negative_image

    def average_image(self):
        if self.image is None:
            print("Error: No image loaded")
            return
        kernel_size, ok = QInputDialog.getInt(self, "Input", "Enter kernel size:", min=1, max=20)
        if not ok:
            return
        open_cv_image = np.array(self.image.convert("RGB"))
        averaged_image = cv2.blur(open_cv_image, (kernel_size, kernel_size))
        averaged_image = Image.fromarray(cv2.cvtColor(averaged_image, cv2.COLOR_BGR2RGB))
        self.display_image(averaged_image)
        self.image = averaged_image

    def draw_rectangle(self):
        if self.image is None:
            print("Error: No image loaded")
            return
        try:
            x1, ok1 = QInputDialog.getInt(self, "Input", "Enter x1 coordinate:", min=0, max=self.image.width)
            y1, ok2 = QInputDialog.getInt(self, "Input", "Enter y1 coordinate:", min=0, max=self.image.height)
            x2, ok3 = QInputDialog.getInt(self, "Input", "Enter x2 coordinate:", min=0, max=self.image.width)
            y2, ok4 = QInputDialog.getInt(self, "Input", "Enter y2 coordinate:", min=0, max=self.image.height)
            if not (ok1 and ok2 and ok3 and ok4):
                return
            open_cv_image = np.array(self.image.convert("RGB"))
            cv2.rectangle(open_cv_image, (x1, y1), (x2, y2), (0, 0, 255), 2)
            rectangled_image = Image.fromarray(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB))
            self.display_image(rectangled_image)
            self.image = rectangled_image
        except Exception as e:
            print(f"Error: Failed to draw rectangle: {str(e)}")

    def show_color_channel(self, channel):
        if self.image is None:
            print("Error: No image loaded")
            return
        if self.channel_displayed == channel:
            self.display_image(self.original_image)
            self.image = self.original_image.copy()
            self.channel_displayed = None
        else:
            try:
                open_cv_image = np.array(self.image.convert("RGB"))
                zeros = np.zeros_like(open_cv_image)
                channel_image = zeros.copy()
                if channel == 'red':
                    channel_image[:, :, 0] = open_cv_image[:, :, 0]
                elif channel == 'green':
                    channel_image[:, :, 1] = open_cv_image[:, :, 1]
                elif channel == 'blue':
                    channel_image[:, :, 2] = open_cv_image[:, :, 2]
                channel_image = Image.fromarray(channel_image)
                self.display_image(channel_image)
                self.image = channel_image
                self.channel_displayed = channel
            except Exception as e:
                print(f"Error: Failed to show color channel: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageApp()
    window.show()
    sys.exit(app.exec_())
