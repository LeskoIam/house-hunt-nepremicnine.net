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

        item["region"] = self.get_region(response)
        item["administrative_unit"] = "na"
        item["municipality"] = "na"
        item["url"] = response.url
        item["price"] = self.get_price(response)
        item["seller"] = self.get_seller(response)
        item["house_area"], item["land_area"], item["settlement"], item["type_"] = self.get_listing_basic_data(response)
        yield item

    @staticmethod
    def get_price(response):
        raw = response.xpath("//div[@class='price']/span/text()").extract()[0]
        cooked = float(raw.replace("€", "").replace(".", "").replace(",", ".").strip())
        return cooked

    @staticmethod
    def get_seller(response):
        try:
            raw = response.xpath("//div[@id='sellerInfo']/div[@class='box']/p[2]/strong/text()").extract()[0]
        except IndexError as err:
            # raw = response.xpath("//div[@id='sellerInfo']/div/p[1]/strong/text()").extract()[0]
            raw = "ZP"
        cooked = raw.strip()
        return cooked

    @staticmethod
    def get_region(response):
        raw = response.xpath("//table[@class='oglas-podatki']/tr[1]/td[2]/b/text()").extract()[0]
        return raw

    @staticmethod
    def get_listing_basic_data(response):
        field_names = response.xpath("//table[@class='oglas-podatki']/tr/td[1]/text()").extract()

        field_names = [x for x in field_names if len(x) > 3]

        print(field_names)
        field_data_indexes = {}
        for i, field_name in enumerate(field_names, start=1):
            field_name = field_name.lower()
            if "velikost" in field_name:
                field_data_indexes["velikost"] = i
            elif "parcela" in field_name:
                field_data_indexes["parcela"] = i
            elif "kraj:" in field_name:
                field_data_indexes["naselje"] = i
            elif "tip hiše" in field_name:
                field_data_indexes["type"] = i

        print(field_data_indexes)
        raw_house_area = response.xpath(f"//table[@class='oglas-podatki']/tr[{field_data_indexes.get('velikost', -1)}]/td[2]/b/text()").extract()[0]
        raw_land_area = response.xpath(f"//table[@class='oglas-podatki']/tr[{field_data_indexes.get('parcela', -1)}]/td[2]/b/text()").extract()[0]
        raw_settlement = response.xpath(f"//table[@class='oglas-podatki']/tr[{field_data_indexes.get('naselje', -1)}]/td[2]/b/text()").extract()[0]
        raw_type = response.xpath(f"//table[@class='oglas-podatki']/tr[{field_data_indexes.get('type', -1)}]/td[2]/b/text()").extract()[0]

        cooked_house_area = float(raw_house_area.replace("m2", "").replace(",", ".").strip())
        cooked_land_area = float(raw_land_area.replace("m2", "").replace(",", ".").strip())
        cooked_settlement = raw_settlement.strip()
        cooked_type = raw_type.strip()

        return cooked_house_area, cooked_land_area, cooked_settlement, cooked_type
