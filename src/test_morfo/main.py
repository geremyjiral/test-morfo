import logging
from time import time
import pandas as pd

from test_morfo.image_generator import generate_image_batches
from test_morfo.shapes_creator import add_square_to_image
from test_morfo.cropping import random_crop_image
from test_morfo.color_stats import analyze_images_color_stats
from test_morfo.aws_uploader import upload_batches_stats_to_s3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

black_color = (0, 0, 0)
white_color = (255, 255, 255)
square_size = 50


def main(aws: bool = False):
    """
    Main function to generate image batches.
    """

    images = generate_image_batches()
    batches_stats = pd.DataFrame(
        columns=[
            "batch_id",
            "white_avg",
            "white_std",
            "white_min",
            "white_max",
            "black_avg",
            "black_std",
            "black_min",
            "black_max",
        ]
    )
    for batch in images:
        batch_dir = batch[0][0].parent.parent
        batch_name = batch_dir.name
        batch_square_dir = batch_dir / "square"
        batch_square_dir.mkdir(parents=True, exist_ok=True)

        batch_cropped_dir = batch_dir / "cropped"
        batch_cropped_dir.mkdir(parents=True, exist_ok=True)

        for img_path, img in batch:
            # Add a square to the image and save it
            previous_img, previous_shape = add_square_to_image(
                img, black_color, [], size=square_size
            )
            first_img_path = batch_square_dir / (img_path.stem + "_squared.png")
            previous_img.save(first_img_path)
            # Add a second square to the image without overlapping and save it
            second_img, _ = add_square_to_image(
                previous_img, black_color, [previous_shape], size=square_size
            )
            second_img_path = batch_square_dir / (img_path.stem + "_squared_second.png")
            second_img.save(second_img_path)
            logger.info(
                f"Processed squared images: {first_img_path}, {second_img_path}"
            )
            # Crop the image randomly and save it
            cropped_img = random_crop_image(second_img)
            cropped_img_path = batch_cropped_dir / (img_path.stem + "_cropped.png")
            cropped_img.save(cropped_img_path)
            logger.info(f"Processed cropped image: {cropped_img_path}")

        # Analyze color statistics for the processed images
        start_time = time()
        color_stats = analyze_images_color_stats(batch_dir.name, batch, black_color)
        logger.info(f"Color statistics for black color: {color_stats}")

        # Analyze color statistics for white color
        white_color_stats = analyze_images_color_stats(batch_name, batch, white_color)
        logger.info(f"Color statistics for white color: {white_color_stats}")
        end_time = time()
        logger.info(
            f"Batch {batch_name} processed in {end_time - start_time:.2f} seconds."
        )

        efficiency_threshold = 100_000
        start_time = time()
        color_stats = analyze_images_color_stats(
            batch_name, batch, black_color, efficiency_threshold
        )
        logger.info(f"Color statistics for black color: {color_stats}")

        # Analyze color statistics for white color
        white_color_stats = analyze_images_color_stats(
            batch_name, batch, white_color, efficiency_threshold
        )
        logger.info(f"Color statistics for white color: {white_color_stats}")
        end_time = time()
        total_time = end_time - start_time
        logger.info(
            f"Batch {batch_name} processed in {total_time:.2f} seconds with efficiency."
        )
        batches_stats = pd.concat(
            [
                batches_stats,
                pd.DataFrame(
                    [
                        [
                            batch_name,
                            white_color_stats.avg,
                            white_color_stats.std,
                            white_color_stats.min,
                            white_color_stats.max,
                            color_stats.avg,
                            color_stats.std,
                            color_stats.min,
                            color_stats.max,
                        ]
                    ],
                    columns=batches_stats.columns,
                ),
            ],
            ignore_index=True,
        )
    if aws:
        upload_batches_stats_to_s3(batches_stats)
    else:
        batches_stats.to_parquet("output/batches_stats.parquet", engine="pyarrow")


if __name__ == "__main__":
    main()
