from typing import List

from pydantic import BaseModel

from search_module.schema.attribute import AttributeDTO


class SearchRequestDTO(BaseModel):
    image_base64: str
    semantic_attributes: List[AttributeDTO]
