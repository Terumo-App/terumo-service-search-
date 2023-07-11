from abc import ABC, abstractmethod
from typing import List, Tuple


class SemanticExtractorInterface(ABC):
    """
    The Semantic Extractor interface declares the operations that all concrete s Semantic Extractor
    must implement.
    """

    @abstractmethod
    def extract(self, search_data) -> Tuple[List[int], List[str]]:
        pass
