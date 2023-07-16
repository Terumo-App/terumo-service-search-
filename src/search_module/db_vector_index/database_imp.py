import os
from typing import List, Tuple

import numpy as np
import pandas as pd
from scipy.spatial import distance

from src.search_module.db_vector_index.vector_db_interface import (
    VectorDBInterface,
)

PATH_PREFIX = 'src/' if os.getenv('ON_CONTAINER') else ''

DB_LOCATION = (
    f'{PATH_PREFIX}search_module/db_vector_index/db_binary_vector.npy'
)
METADATA_LOCATION = (
    f'{PATH_PREFIX}search_module/db_vector_index/image_db_index.csv'
)


class VectorDBImp(VectorDBInterface):
    def __init__(self):
        self.db = np.load(DB_LOCATION)
        self.metadata = pd.read_csv(METADATA_LOCATION)

    def retrieve(
        self, query: List[int], atts: List[str], k: int
    ) -> List[Tuple[int, float, str]]:
        """return k most similar data from given DB. For the following similarity search
        is considered jaccard distance.
        """
        vector_dim = 6
        if len(query) != vector_dim:
            raise Exception(
                f'Query vector should have dim 6. Found dim {len(query)}'
            )

        # TODO set correct_att properly once we define the order of atts
        for correct_att, query_att in zip(atts, atts):
            if correct_att != query_att:
                raise Exception(
                    f'Query attributes are in wrong order. They shoud be like this: {atts}.'
                )

        dist = np.array([distance.jaccard(query, i) for i in self.db])
        ordered_ids = np.argsort(dist)[:k]
        ordered_dist = dist[ordered_ids]

        result_set = [
            (id, dis, path)
            for path, id, dis in zip(
                self.metadata['file'].iloc[list(ordered_ids)],
                ordered_ids,
                ordered_dist,
            )
        ]

        return result_set
