from ..secret import host, port, db, user, password, dialct, driver

from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

url = f"{dialct}+{driver}://{user}:{password}@{host}:{port}/{db}"

Base = declarative_base()
engine = create_engine(url)
Session = sessionmaker(engine)


def create_all():
    return Base.metadata.create_all(engine)


session = Session()
