from PIL import ImageDraw, Image
import random


def add_square_to_image(
    image: Image.Image,
    color: tuple[int, int, int],
    used_areas: list[tuple[int, int, int, int]],
    size: int = 50,
    max_attempts: int = 100,
) -> tuple[Image.Image, tuple[int, int, int, int]]:
    """
    Add a colored square to an image in a non-overlapping area.

    :param image: Image PIL to modify.
    :param square_size: Size (in pixels) of the square (square = width = height).
    :param color: RGB color of the square.
    :param used_areas: List of already used areas [(x1, y1, x2, y2)].
    :param include_area: Area (x1, y1, x2, y2) in which the square must be placed.
    :param exclude_areas: Areas in which drawing is not allowed.
    :param max_attempts: Maximum number of attempts to place the square.
    :return: Modified image and coordinates of the square [(x1, y1, x2, y2)].
    """

    width, height = image.size
    draw = ImageDraw.Draw(image)
    include_area = (0, 0, width, height)

    for _ in range(max_attempts):
        x1 = random.randint(include_area[0], include_area[2] - size)
        y1 = random.randint(include_area[1], include_area[3] - size)
        x2, y2 = x1 + size, y1 + size
        proposed = (x1, y1, x2, y2)

        # Check overlap with used areas
        if any(overlaps(proposed, ua) for ua in used_areas):
            continue

        draw.rectangle(proposed, fill=color)
        return image, proposed

    raise ValueError(
        "Impossible to place a square without overlap after several attempts."
    )


def overlaps(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> bool:
    """Returns True if two rectangles overlap."""
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    return not (ax2 <= bx1 or ax1 >= bx2 or ay2 <= by1 or ay1 >= by2)
