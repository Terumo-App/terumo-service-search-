import os
from typing import List, Tuple

from fastapi import UploadFile

from src.search_module.binary_models.binary_extractor_imp import (
    BinaryExtractor,
)
from src.search_module.db_sqllite.sqllite_db_imp import SQLLiteDBImp
from src.search_module.db_vector_index.database_imp import VectorDBImp
from src.search_module.schema.attribute import AttributeDTO
from src.search_module.schema.image import ImageResponse
from src.search_module.schema.search_request import SearchRequestDTO

BINARY_EXTRACTOR = BinaryExtractor()
DB_INDEX = VectorDBImp()
SQLLite = SQLLiteDBImp()
API_BASE_PATH = (
    os.getenv('API_BASE_PATH')
    if os.getenv('API_BASE_PATH')
    else 'http://localhost:5000/image-service/glomerulos/'
)


class SearchService:
    @staticmethod
    def get_semantic_attributes_available():
        att = [
            AttributeDTO(id='normal', name='Normal'),
            AttributeDTO(id='hypercellularity', name='Hypercellularity'),
            AttributeDTO(id='podocytopathy', name='Podocytopathy'),
            AttributeDTO(id='membranous', name='Membranous'),
            AttributeDTO(id='crescent', name='Crescent'),
            AttributeDTO(id='sclerosis', name='Sclerosis'),
        ]
        return att

    @staticmethod
    def search(search_data: SearchRequestDTO):
        semantic_vector, atts = SearchService._extract_semantic_vector(
            search_data
        )
        # embeddings_vector = SearchService._extract_embeddings(search_data)
        image_result = SearchService._retrieve_k_similar(
            vector=semantic_vector, atts=atts, k=100
        )

        return image_result

    @staticmethod
    def upload_query_image(file: UploadFile):
        location = SearchService._save_image_on_file_storage(file)
        image_id = SearchService._save_image_metadata(file, location)
        print(file.filename)
        return image_id

    @staticmethod
    def _save_image_on_file_storage(image: UploadFile) -> str:
        """This function is responsible for saving image in file storage used by the app"""
        file_location = f'image_storage/{image.filename}'
        with open(file_location, 'wb') as f:
            f.write(image.file.read())

        return file_location

    @staticmethod
    def _save_image_metadata(file: UploadFile, location: str) -> int:
        """This function is responsible for extract binary vector from image"""

        return SQLLite.save_image(file, location)

    @staticmethod
    def _extract_semantic_vector(search_data: SearchRequestDTO):
        """This function is responsible for extract binary vector from image"""
        return BINARY_EXTRACTOR.extract(search_data)

    @staticmethod
    def _extract_embeddings(search_data: SearchRequestDTO):
        """This function is responsible for extract n dim embeddings vector from image"""
        return ''

    @staticmethod
    def _retrieve_k_similar(
        vector: List[int], atts: List[str], k: int
    ) -> List[Tuple[int, float, str]]:
        """This functions execute query by given similarity mesure"""
        result = DB_INDEX.retrieve(vector, atts, k)
        result = [
            ImageResponse(id=id, distance=dis, image_url=API_BASE_PATH + path)
            for id, dis, path in result
        ]
        return result
