from pydantic import BaseModel


class ImageDimensions(BaseModel):
    width: int
    height: int


class ColorStats(BaseModel):
    batch_id: str
    avg: float
    std: float
    min: int
    max: int
