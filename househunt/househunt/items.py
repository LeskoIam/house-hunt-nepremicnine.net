# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HousehuntItem(scrapy.Item):
    url = scrapy.Field()
    type_ = scrapy.Field()
    region = scrapy.Field()
    administrative_unit = scrapy.Field()  # Upravna enota
    municipality = scrapy.Field()         # Obcina
    price = scrapy.Field()
    seller = scrapy.Field()               # Prodajalec ZP - zasebna ponudba
    settlement = scrapy.Field()           # Naselje
    house_area = scrapy.Field()



