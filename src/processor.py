import cv2

class Processor:
    def __init__(self):
        pass

    def process_photo(self, photo_path):
        image = cv2.imread(photo_path)  
        if image is None:
            raise ValueError("Image not found or unable to read the image.")

        blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
        return blurred_image
        pass