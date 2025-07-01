import boto3
from io import BytesIO
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def upload_batches_stats_to_s3(batches_stats: pd.DataFrame) -> None:
    s3 = boto3.client("s3")
    buffer = BytesIO()
    batches_stats.to_parquet(buffer, index=False, engine="pyarrow")
    buffer.seek(0)
    bucket = "your-bucket-name"
    key = "test/test.parquet"
    s3.upload_fileobj(buffer, Bucket=bucket, Key=key)

    logger.info(f"Uploaded to s3://{bucket}/{key}")
