from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from .constants import URL_BOLHA, DOMAIN_BOLHA
from ..items import HousehuntItem


class ExampleSpider(CrawlSpider):
    name = 'bolha'
    allowed_domains = [DOMAIN_BOLHA]
    start_urls = [URL_BOLHA]

    rules = (
        # Crawl items
        Rule(LinkExtractor(restrict_xpaths="//div[@class='ad']/div[@class='coloumn content']/h3/a"),
             callback="parse_single_listing"),
        # Crawl "next" pages
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='forward'])[1]")),
    )

    def parse_single_listing(self, response):
        item = HousehuntItem()

        price = self.get_price(response)

        # _, type_, regija, upravna_enota, obcina = self.get_basic_info(response)
        #
        # item["type_"] = type_
        # item["region"] = regija
        # item["administrative_unit"] = upravna_enota.replace(",", "")
        # item["municipality"] = obcina
        # item["url"] = response.url
        # item["price"] = self.get_price(response)
        # item["seller"] = self.get_seller(response)
        # item["settlement"] = self.get_settlement(response)
        # item["house_area"], item["land_area"] = self.get_house_and_land_area(response)
        #
        # yield item

    def get_price(self, response):
        raw = response.xpath("//div[@class='price']/span/text()").extract()
        print("######"*4)
        print(raw)
        print("######" * 4)
        return raw


    # @staticmethod
    # def get_basic_info(response):
    #     """
    #     Vrsta
    #     Regija
    #     Upravna enota
    #     Obcina
    #     """
    #
    #     raw = response.xpath("//div[@class='more_info'][contains(.,'Posredovanje')]/text()").extract()
    #
    #     raw = raw[0].split("|")
    #     out = []
    #     for data in raw:
    #         data = data.split(":")[-1].strip()
    #         out.append(data)
    #     return out
    #
    # @staticmethod
    # def get_price(response):
    #     raw = response.xpath("//div[@class='cena clearfix']/span/text()").extract()[0]
    #     if "cca" in raw.lower():
    #         raw = raw.replace("cca", "")
    #     if "do" in raw.lower():
    #         raw = raw.replace("do", "")
    #     try:
    #         price = float(raw.replace("€", "").replace(".", "").replace(",", ".").strip())
    #     except ValueError as err:
    #         price = -1.
    #     return price
    #
    # @staticmethod
    # def get_seller(response):
    #     raw = response.xpath("//div[@class='prodajalec']/h2/text()").extract()[0]
    #     if "zasebna" in raw.lower():
    #         raw = "ZP"
    #     return raw
    #
    # @staticmethod
    # def get_settlement(response):
    #     return response.xpath("//div[@class='kratek']/strong[@class='rdeca']/text()").extract()[0]
    #
    # @staticmethod
    # def get_house_and_land_area(response):
    #     raw = response.xpath("//div[@class='kratek']/text()").extract()[0]
    #     try:
    #         house_area = float(raw.split("m2")[0][1:].replace(",", ".").strip())
    #     except ValueError as err:
    #         house_area = -1.
    #
    #     try:
    #         land_area = int(raw.split("m2")[1].split(",")[-1].replace(".", ""))
    #     except ValueError as err:
    #         land_area = -1
    #
    #     return house_area, land_area
