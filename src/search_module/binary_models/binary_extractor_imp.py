from typing import List, Tuple
from search_module.binary_models.binary_extractor_interface import SemanticExtractorInterface
from search_module.binary_models.binary_base_model import ModelInfer
# from search_module.service import SearchRequestDTO


from PIL import Image
import base64
import io

MODELS = [
    ModelInfer('HIPER'),
    ModelInfer('MEMBR'),
    ModelInfer('NORM'),
    ModelInfer('SCLER'),
    ModelInfer('PODOC'),
    ModelInfer('CRESC'),
]
MODELS_NAME = [
    'hypercellularity',
    'membranous',
    'normal',
    'sclerosis',
    'podocytopathy',
    'crescent',
]


class BinaryExtractor(SemanticExtractorInterface):
    def extract(self, search_data) -> Tuple[List[int], List[str]]:

        vector = []
        att = []

        att_to_be_searched = [i.id for i in search_data.semantic_attributes]
        image = self._convert_base64_to_image(search_data.image_base64)

        for model, name in zip(MODELS, MODELS_NAME):
            if name in att_to_be_searched:

                vector.append(model.predict(model.process(image)))
                att.append(name)

        return vector, att

    def _convert_base64_to_image(self, image_base64: str) -> Image.Image:
        """ this function decodes base64 image data to binary and afeter that convert it
        for Pillow image object.

        Args:
            image (str): image encoded in base64

        Returns:
            PIL.PngImagePlugin.PngImageFile

        """
        # Decode base64 image data
        image_data = base64.b64decode(image_base64)
        # Convert bytes to image object
        return Image.open(io.BytesIO(image_data))
