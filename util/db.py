from ..secret import host, port, db, user, password, dialct, driver

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker

uri = f"{dialct}+{driver}://{user}:{password}@{host}:{port}/{db}"


