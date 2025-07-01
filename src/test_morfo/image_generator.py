import numpy as np
from PIL import Image
import logging
from pathlib import Path
from test_morfo.models import ImageDimensions


logger = logging.getLogger(__name__)
default_dimensions = ImageDimensions(width=256, height=512)


def generate_image_batches(
    save_dir: Path = Path("output"),
    size: ImageDimensions = default_dimensions,
    batch_count: int = 5,
    images_per_batch: int = 20,
) -> list[list[tuple[Path, Image.Image]]]:
    """
    Generate batches of images and save them to the specified directory.
    :param save_dir: Directory to save the generated images.
    :param size: Dimensions of the images to generate.
    :param batch_count: Number of batches to generate.
    :param images_per_batch: Number of images per batch.
    :return: List of batches, each containing tuples of (image path, image object).
    """

    save_dir.mkdir(parents=True, exist_ok=True)
    images: list[list[tuple[Path, Image.Image]]] = []
    for batch_idx in range(batch_count):
        batch_dir = save_dir / f"batch_{batch_idx + 1}" / "original"
        batch_dir.mkdir(parents=True, exist_ok=True)
        batch_images: list[tuple[Path, Image.Image]] = []
        for img_idx in range(images_per_batch):
            path, img = generate_image(batch_dir / f"img_{img_idx + 1}.png", size)
            batch_images.append((path, img))
        logger.info(f"✅ Batch {batch_idx + 1} created with {images_per_batch} images.")
        images.append(batch_images)
    return images


def generate_image(
    path: Path, size: ImageDimensions = default_dimensions, colors: int = 3
) -> tuple[Path, Image.Image]:
    img_array = np.random.randint(
        0, size.width, (size.width, size.height, colors), dtype=np.uint8
    )
    img = Image.fromarray(img_array, "RGB")
    img.save(path)
    return path, img
