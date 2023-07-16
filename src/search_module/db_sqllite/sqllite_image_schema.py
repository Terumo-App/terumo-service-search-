from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
Base = declarative_base()

class ImageDAO(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String)
    filepath = Column(String)