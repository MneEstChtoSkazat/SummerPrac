import cv2
import numpy as np
from PIL import Image, ImageOps, ImageTk
from tkinter import messagebox, simpledialog

from PyQt5.QtWidgets import QInputDialog


def capture_from_webcam(self):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Failed to connect to the webcam")
        return

    ret, frame = cap.read()
    cap.release()
    if not ret:
        messagebox.showerror("Error", "Failed to capture image")
        return

    self.image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    self.display_image(self.image)

def display_image(self, image):
    image.thumbnail((800, 600))
    photo = ImageTk.PhotoImage(image)
    self.image_label.config(image=photo)
    self.image_label.image = photo

def show_negative(self):
    if self.image is None:
        messagebox.showerror("Error", "No image loaded")
        return
    negative_image = ImageOps.invert(self.image.convert("RGB"))
    self.display_image(negative_image)
    self.image = negative_image

def average_image(self):
    if self.image is None:
        messagebox.showerror("Error", "No image loaded")
        return
    try:
        kernel_size = simpledialog.askinteger("Input", "Enter kernel size:", minvalue=1, maxvalue=20)
        if kernel_size is None:
            return
        open_cv_image = np.array(self.image.convert("RGB"))
        averaged_image = cv2.blur(open_cv_image, (kernel_size, kernel_size))
        averaged_image = Image.fromarray(cv2.cvtColor(averaged_image, cv2.COLOR_BGR2RGB))
        self.display_image(averaged_image)
        self.image = averaged_image
    except Exception as e:
        messagebox.showerror("Error", f"Failed to average image: {str(e)}")

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
        messagebox.showerror("Error", "No image loaded")
        return
    try:
        channels = {"red": 0, "green": 1, "blue": 2}
        if channel not in channels:
            messagebox.showerror("Error", "Invalid color channel")
            return

        # Если текущий канал совпадает с запрашиваемым, показываем исходное изображение
        if self.channel_displayed == channel:
            self.display_image(self.original_image)
            self.image = self.original_image.copy()
            self.channel_displayed = None
            return

        # Показываем выбранный цветной канал
        open_cv_image = np.array(self.image.convert("RGB"))
        zeros = np.zeros_like(open_cv_image)
        channel_image = zeros.copy()
        channel_image[:, :, channels[channel]] = open_cv_image[:, :, channels[channel]]
        channel_image = Image.fromarray(channel_image)
        self.display_image(channel_image)
        self.image = channel_image
        self.channel_displayed = channel

    except Exception as e:
        messagebox.showerror("Error", f"Failed to show color channel: {str(e)}")
