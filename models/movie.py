from config.dabatase import Base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

class Movie(Base):

    __tablename__ = "movies"

    id = Column(Integer, primary_key= True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)
