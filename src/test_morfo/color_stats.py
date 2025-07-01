from PIL import Image
import numpy as np
from test_morfo.models import ColorStats
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def count_color_pixels(img_array: np.ndarray, color: tuple[int, int, int]) -> int:
    """Count the number of pixels matching the given RGB color."""
    return int(np.sum(np.all(img_array == color, axis=-1)))


def count_color_pixels_efficient(image_path: Path, color: tuple[int, int, int]) -> int:
    """Efficiently count white and black pixels using pixel access."""
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        width, height = img.size
        count = 0

        pixels = img.load()  # type: ignore
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]  # type: ignore
                if (r, g, b) == color:
                    count += 1
    return count


def analyze_images_color_stats(
    batch_id: str,
    images: list[tuple[Path, Image.Image]],
    color: tuple[int, int, int],
    efficiency_threshold: float = 200_000,
) -> ColorStats:
    """
    Analyze the color statistics of a list of images for a specific RGB color.
    :param images: List of PIL Image objects.
    :param color: RGB color to analyze.
    :return: ColorStats object containing average, std, min, and max pixel counts.
    """
    pixels: list[int] = []
    for img in images:
        if img[1].size[0] * img[1].size[1] > efficiency_threshold:
            pixels.append(count_color_pixels_efficient(img[0], color))
        else:
            arr = np.array(img[1])
            pixels.append(count_color_pixels(arr, color))
    return ColorStats(
        batch_id=batch_id,
        avg=float(np.mean(pixels)),
        std=float(np.std(pixels)),
        min=np.min(pixels),
        max=np.max(pixels),
    )
