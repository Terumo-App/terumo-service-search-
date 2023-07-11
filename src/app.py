from fastapi import FastAPI, File, UploadFile, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging
import argparse
import uvicorn
from typing import List
from search_module.schema.image import ImageResponse

from search_module.schema.search_request import SearchRequestDTO 
from search_module.service import SearchService
from image_module.service import ImageService


logging.getLogger().setLevel(logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=8000, help="Port number")
parser.add_argument("--reload",type=bool, default=True, help="Reaload API when file is change")

args = parser.parse_args()
port = args.port
reload = args.reload


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

    

############################### Image Service ###############################

IMAGE_PATH = 'C:/Users/Maods/Documents/Development/Mestrado/terumo/apps/terumo-model-binary-glomerulus-hypercellularity/data/raw/'
app.mount("/image-service/glomerulos", StaticFiles(directory=IMAGE_PATH), name="images")

@app.get("/image-service/collection/")
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
@app.get("/search-service/semantic-attributes/")
async def get_semantic_attributes_available():
    return SearchService.get_semantic_attributes_available()

@app.post("/search-service/search/")
async def search(search_data: SearchRequestDTO) -> List[ImageResponse]:
    return SearchService.search(search_data)






if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=reload)
