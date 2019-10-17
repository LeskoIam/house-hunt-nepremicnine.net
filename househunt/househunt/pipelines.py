# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from .database import RawHousehuntDB, db_connect, create_table


class HousehuntPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.
        """
        session = self.Session()
        db = RawHousehuntDB()

        db.url = item["url"]
        db.type_ = item["type_"]
        db.region = item["region"]
        db.administrative_unit = item["administrative_unit"]
        db.municipality = item["municipality"]
        db.price = item["price"]
        db.seller = item["seller"]
        db.settlement = item["settlement"]
        db.house_area = item["house_area"]
        db.land_area = item["land_area"]

        try:
            session.add(db)
            session.commit()
        except Exception as exc:
            print(exc)
            session.rollback()
            raise
        finally:
            session.close()

        return item
