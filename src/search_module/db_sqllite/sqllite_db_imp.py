from typing import Dict
import uuid

from fastapi import UploadFile
from sqlalchemy import create_engine, Column, Integer, String, Uuid
from sqlalchemy.orm import declarative_base, sessionmaker

from src.search_module.db_sqllite.sqllite_db_interface import SQLLiteDBInterface
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.search_module.db_sqllite.sqllite_image_schema import ImageDAO

DB_PATH = "sqlite:///image_database.db"

base = declarative_base()


class ImageDAO(base):
    __tablename__ = "images"

    id = Column(Uuid, primary_key=True)
    filename = Column(String)
    filepath = Column(String)


class SQLLiteDBImp(SQLLiteDBInterface):

    def __init__(self):
        self.engine = create_engine(DB_PATH, echo=True)
        self.session = None
        self.setup()

    def setup(self):
        base.metadata.create_all(bind=self.engine)
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def get_image_path(self, image_id: str):
        image_data = self.session.query(ImageDAO).filter_by(id=uuid.UUID(image_id)).first()

        if not image_data:
            return Exception('Image not found in SQL Lite')

        return {
            "id": image_data.id,
            "filename": image_data.filename,
            "filepath": image_data.filepath,
        }

    def save_image(self, image: UploadFile, file_location: str) -> Dict[str, int]:
        image_id = uuid.uuid4()
        image_data = ImageDAO(id=image_id, filename=image.filename, filepath=file_location)
        self.session.add(image_data)
        self.session.commit()
        return {"id": image_data.id}
