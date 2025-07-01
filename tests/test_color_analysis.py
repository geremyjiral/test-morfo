import numpy as np
import pytest
from PIL import Image
from pathlib import Path
from test_morfo.color_stats import count_color_pixels


@pytest.fixture
def white_image(tmp_path: Path) -> Path:
    path = tmp_path / "white.png"
    img = Image.new("RGB", (10, 10), color=(255, 255, 255))  # 100 white pixels
    img.save(path)
    return path


def test_white_pixel_count(white_image: Path):
    arr = np.array(Image.open(white_image))
    count = count_color_pixels(arr, (255, 255, 255))
    assert count == 100


def test_corrupted_image(tmp_path: Path):
    corrupted_path = tmp_path / "corrupted.png"
    corrupted_path.write_bytes(b"notarealimage")

    with pytest.raises(Exception):
        count_color_pixels(np.array(Image.open(corrupted_path)), (255, 255, 255))
