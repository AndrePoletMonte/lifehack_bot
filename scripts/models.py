from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    username = Column(String, nullable=True)
    language = Column(String(2), default="en")

class Lifehack(Base):
    __tablename__ = "lifehacks"

    id = Column(Integer, primary_key=True, index=True)
    text_en = Column(String, nullable=False)
    text_sr = Column(String, nullable=False)