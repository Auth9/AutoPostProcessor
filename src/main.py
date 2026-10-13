import shutil
import subprocess
import sys
from pathlib import Path

import cv2


class ImageProcessor:
    def _linux_file_dialog(self, title, initial_path, save=False):
        if shutil.which("zenity"):
            command = [
                "zenity",
                "--file-selection",
                f"--title={title}",
                f"--filename={initial_path}",
                "--file-filter=Image files | *.bmp *.gif *.jpeg *.jpg *.png *.tif *.tiff",
                "--file-filter=All files | *",
            ]
            if save:
                command.extend(("--save", "--confirm-overwrite"))
        elif shutil.which("kdialog"):
            command = ["kdialog"]
            command.append("--getsavefilename" if save else "--getopenfilename")
            command.extend(
                (
                    str(initial_path),
                    "Image files (*.bmp *.gif *.jpeg *.jpg *.png *.tif *.tiff)",
                    "--title",
                    title,
                )
            )
        else:
            raise RuntimeError(
                "No desktop file dialog is available. Install zenity or kdialog."
            )

        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode:
            if result.stderr.strip():
                raise RuntimeError(f"File dialog failed: {result.stderr.strip()}")
            return None

        selected_path = result.stdout.strip()
        return Path(selected_path) if selected_path else None

    def _native_file_dialog(self, title, initial_path, save=False):
        if sys.platform.startswith("linux"):
            return self._linux_file_dialog(title, initial_path, save)

        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        try:
            dialog = (
                filedialog.asksaveasfilename
                if save
                else filedialog.askopenfilename
            )
            options = {
                "title": title,
                "initialdir": str(initial_path.parent if save else initial_path),
                "filetypes": (
                    ("Image files", "*.bmp *.gif *.jpeg *.jpg *.png *.tif *.tiff"),
                    ("All files", "*.*"),
                ),
            }
            if save:
                options["initialfile"] = initial_path.name
                options["defaultextension"] = initial_path.suffix or ".png"
            selected_path = dialog(**options)
        finally:
            root.destroy()

        return Path(selected_path) if selected_path else None

    def choose_image(self):
        return self._native_file_dialog(
            "Select an image to process", Path.home()
        )

    def choose_output_path(self, image_path):
        image_path = Path(image_path)
        extension = image_path.suffix or ".png"
        default_path = image_path.with_name(
            f"processed_{image_path.stem}{extension}"
        )
        return self._native_file_dialog(
            "Save processed image", default_path, save=True
        )

    def process_image(self, image_path, output_path=None, save_processed=False):
        image_path = Path(image_path)
        if not image_path.is_file():
            raise FileNotFoundError(f"Image file not found: {image_path}")

        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Unable to read image: {image_path}")

        processed = cv2.GaussianBlur(image, (5, 5), 0)

        if save_processed:
            output_path = (
                Path(output_path)
                if output_path
                else image_path.with_name(f"processed_{image_path.name}")
            )
            output_path.parent.mkdir(parents=True, exist_ok=True)
            if not cv2.imwrite(str(output_path), processed):
                raise OSError(f"Unable to save processed image to: {output_path}")
            return processed, output_path

        return processed

    def run(self):
        image_path = self.choose_image()
        if image_path is None:
            print("No image selected.")
            return None

        output_path = self.choose_output_path(image_path)
        if output_path is None:
            print("Save cancelled.")
            return None

        _, saved_path = self.process_image(
            image_path, output_path=output_path, save_processed=True
        )
        print(f"Processed image saved to: {saved_path}")
        return saved_path


if __name__ == "__main__":
    ImageProcessor().run()
