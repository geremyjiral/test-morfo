from PIL import Image
import random
from test_morfo.models import ImageDimensions


def random_crop_image(
    image: Image.Image,
    crop_size: ImageDimensions = ImageDimensions(height=200, width=200),
) -> Image.Image:
    """
    Crop a random area from the input image.

    :param image: Image PIL input.
    :param crop_size: Desired crop dimensions.
    :return: Cropped PIL image.
    """
    img_width, img_height = image.size

    if crop_size.width > img_width or crop_size.height > img_height:
        raise ValueError(
            f"Crop size {crop_size} is larger than image size {image.size}."
        )

    max_x = img_width - crop_size.width
    max_y = img_height - crop_size.height

    x1 = random.randint(0, max_x)
    y1 = random.randint(0, max_y)
    x2 = x1 + crop_size.width
    y2 = y1 + crop_size.height

    return image.crop((x1, y1, x2, y2))
