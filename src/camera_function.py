import cv2
from PIL import Image

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
