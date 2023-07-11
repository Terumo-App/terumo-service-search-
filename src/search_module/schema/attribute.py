
from pydantic import BaseModel
from typing import List




class AttributeDTO(BaseModel):
    id: str
    name: str