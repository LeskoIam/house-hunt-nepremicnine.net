import datetime

from scrapy.utils.project import get_project_settings
from sqlalchemy import (
    Integer, String, DateTime, Float, Text)
from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class RawHousehuntDB(DeclarativeBase):

    """url = scrapy.Field()
    type_ = scrapy.Field()
    region = scrapy.Field()
    administrative_unit = scrapy.Field()  # Upravna enota
    municipality = scrapy.Field()         # Obcina
    price = scrapy.Field()
    seller = scrapy.Field()               # Prodajalec ZP - zasebna ponudba
    settlement = scrapy.Field()           # Naselje
    house_area = scrapy.Field()
    land_area = scrapy.Field()"""

    __tablename__ = "raw_househunt"

    id = Column(Integer, primary_key=True)

    url = Column("url", Text(), nullable=False)
    type_ = Column("type", String())
    region = Column("region", String())
    administrative_unit = Column("administrative_unit", String())
    municipality = Column("municipality", String())
    price = Column("price", Float())
    seller = Column("seller", String())
    settlement = Column("settlement", String())
    house_area = Column("house_area", Float())
    land_area = Column("land_area", Float())
    description = Column("description", String())

    scraped_on = Column("scraped_on", DateTime(), default=datetime.datetime.utcnow)
