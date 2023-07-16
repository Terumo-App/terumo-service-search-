from abc import ABC, abstractmethod
from typing import List, Tuple


class SQLLiteDBInterface(ABC):
    """
    The Semantic Extractor interface declares the operations that all concrete s Semantic Extractor
    must implement.
    """

    @abstractmethod
    def save_image(self, image):
        pass

    @abstractmethod
    def get_image_path(self, image_id):
        pass
