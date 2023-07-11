from typing import List

from pydantic import BaseModel


class ImageResponse(BaseModel):
    id: int
    distance: float
    image_url: str
