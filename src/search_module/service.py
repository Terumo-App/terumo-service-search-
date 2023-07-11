
from pydantic import BaseModel
from typing import List, Tuple
from search_module.binary_models.binary_extractor_imp import BinaryExtractor
from search_module.schema.attribute import AttributeDTO
from search_module.schema.search_request import SearchRequestDTO
from search_module.schema.image import ImageResponse
from search_module.db_index.database_imp import DatabaseImp


BINARY_EXTRACTOR = BinaryExtractor()
DB_INDEX = DatabaseImp()
API_BASEPATH = 'http://localhost:5000/image-service'

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
        # print([i.id for i in search_data.semantic_attributes])

        semantic_vector, atts = SearchService._extract_semantic_vector(
            search_data)
        # embeddings_vector = SearchService._extract_embeddings(search_data)
        image_result = SearchService._retrieve_k_similar(vector=semantic_vector,
                                                        atts=atts,
                                                        k=100)


        return image_result

    @staticmethod
    def _extract_semantic_vector(search_data: SearchRequestDTO):
        """This functions is responsible for extract binary vector from image
        """
        return BINARY_EXTRACTOR.extract(search_data)

    @staticmethod
    def _extract_embeddings(search_data: SearchRequestDTO):
        """This functions is responsible for extract n dim embeding vector from image
        """
        return ''

    @staticmethod
    def _retrieve_k_similar(vector: List[int], atts: List[str], k: int) -> List[Tuple[int, float, str]]:
        """This functions execute query by given similarity mesure
        """
        result = DB_INDEX.retrieve(vector,atts, k)
        result = [ ImageResponse(id=id,distance=dis, image_url=API_BASEPATH+path) for  id, dis, path in result]
        return result
    
