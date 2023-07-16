import argparse
import logging
import os
from typing import List

import uvicorn
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from image_module.service import ImageService
from search_module.schema.image import ImageResponse
from search_module.schema.search_request import SearchRequestDTO
from search_module.service import SearchService

logging.getLogger().setLevel(logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=5000, help='Port number')
parser.add_argument(
    '--reload', type=bool, default=True, help='Reload API when file is change'
)

args = parser.parse_args()
port = args.port
reload = args.reload


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)


############################### Image Service ###############################
LOCAL_IMAGE_PATH = 'C:/Users/Maods/Documents/Development/Mestrado/terumo/apps/terumo-model-binary-glomerulus-hypercellularity/data/raw/'
CONTAINER_IMAGE_PATH = '/src/db'
IMAGE_PATH = (
    CONTAINER_IMAGE_PATH if os.getenv('ON_CONTAINER') else LOCAL_IMAGE_PATH
)

app.mount(
    '/image-service/glomerulos',
    StaticFiles(directory=IMAGE_PATH),
    name='images',
)


@app.get('/image-service/collection/')
async def get_all_collections():
    return ImageService.get_all_collections()


# @app.get("/image-service/image/collection/{id}")
# async def get_collection(id: int):
#     return ImageService.get_collection()

# @app.post("/image-service/image/collection")
# async def create_collection(item: ImageData):
#     return ImageService.create_collection(ImageData)

# @app.delete("/image-service/image/collection/{id}")
# async def delete_collection(id: int):
#     return ImageService.delete_collection(id)


############################### Search service ###############################
@app.get('/search-service/semantic-attributes/')
async def get_semantic_attributes_available():
    return SearchService.get_semantic_attributes_available()


@app.post('/search-service/upload-query-image/')
async def upload(file: UploadFile = File(...)):
    image_id = SearchService.upload_query_image(file)
    return image_id


@app.post('/search-service/search/')
async def search(search_data: SearchRequestDTO) -> List[ImageResponse]:
    return SearchService.search(search_data)


if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=port, reload=reload)
