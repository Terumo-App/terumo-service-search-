from abc import ABC, abstractmethod
from typing import List, Tuple

class DatabaseInterface(ABC):
    """
    The Semantic Extractor interface declares the operations that all concrete s Semantic Extractor
    must implement.
    """

    @abstractmethod
    def retrieve(self, search_data):
        pass