import cv2


class Input:
    def __init__(self, photo_path=None):
        self.photo_path = photo_path

    def get_photo_path(self):
        if self.photo_path is None:
            raise ValueError("No photo path configured.")
        return self.photo_path

    def load_image(self, image_path):
        self.photo_path = image_path
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not found or unable to read the image.")
        return image