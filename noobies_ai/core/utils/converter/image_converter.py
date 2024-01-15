from PIL import Image


class ImageConverter:
    def __init__(self):
        pass

    def resize(self, image_paths, resolution=(512, 512)):
        """
        Resizes the images in the given image_paths list to the specified resolution.

        Args:
            image_paths (list): List of image file paths.
            resolution (tuple): Tuple representing the target resolution (width, height).

        Returns:
            bool: True if all images are successfully resized and saved, False otherwise.
        """
        try:
            for image_path in image_paths:
                im = Image.open(image_path)
                im = im.resize(resolution)
                im.save(image_path)
            return True
        except Exception as e:
            print(f"Error resizing image: {str(e)}")
            return False
