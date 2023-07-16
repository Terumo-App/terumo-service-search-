from typing import List, Dict

from pydantic import BaseModel

from search_module.schema.attribute import AttributeDTO


class SearchRequestDTO(BaseModel):
    image_metadata: Dict[str, str]
    semantic_attributes: List[AttributeDTO]
