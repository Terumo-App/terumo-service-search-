from datetime import datetime

from pydantic import BaseModel


class CollectionDTO(BaseModel):
    id: str
    name: str
    type: str
    owner: str
    items: int
    last_update: datetime


class ImageService:
    @staticmethod
    def get_all_collections():
        dummy_list = [
            CollectionDTO(
                id='1',
                name='Glomerulos',
                type='Public',
                owner='Matheus',
                items=1000,
                last_update=datetime.today(),
            )
        ]

        return dummy_list
