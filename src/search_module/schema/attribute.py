from typing import List

from pydantic import BaseModel


class AttributeDTO(BaseModel):
    id: str
    name: str
