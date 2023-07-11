
from pydantic import BaseModel
from typing import List

class ImageResponse(BaseModel):
    id: int
    distance: float
    image_url: str