from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from .constants import URLS_NEPREMICNINE, DOMAIN_NEPREMICNINE
from ..items import HousehuntItem


class ExampleSpider(CrawlSpider):
    name = 'nepremicnine'
    allowed_domains = [DOMAIN_NEPREMICNINE]
    start_urls = URLS_NEPREMICNINE

    rules = (
        # Crawl items
        Rule(LinkExtractor(restrict_xpaths="//div[contains(@class, 'oglas_container')]/div/a[contains(@href, 'oglasi-prodaja')]"),
             callback="parse_single_listing"),
        # Crawl "next" pages
        Rule(LinkExtractor(restrict_xpaths="(//div[@id='pagination']/ul/li[@class='paging_next']/a[@class='next'])[1]")),
    )

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.response = None

    def parse_single_listing(self, response):
        self.response = response
        item = HousehuntItem()

        _, type_, regija, upravna_enota, obcina = self.get_basic_info()

        item["type_"] = type_
        item["region"] = regija
        item["administrative_unit"] = upravna_enota.replace(",", "")
        item["municipality"] = obcina
        item["url"] = response.url
        item["price"] = self.get_price()
        item["seller"] = self.get_seller()
        item["settlement"] = self.get_settlement()
        item["house_area"], item["land_area"] = self.get_house_and_land_area()
        item["description"] = self.get_description()

        yield item

    def get_basic_info(self):
        """
        Vrsta
        Regija
        Upravna enota
        Obcina
        """

        raw = self.response.xpath("//div[@class='more_info'][contains(.,'Posredovanje')]/text()").extract()

        raw = raw[0].split("|")
        out = []
        for data in raw:
            data = data.split(":")[-1].strip()
            out.append(data)
        return out

    def get_price(self):
        raw = self.response.xpath("//div[@class='cena clearfix']/span/text()").extract()[0]
        if "cca" in raw.lower():
            raw = raw.replace("cca", "")
        if "do" in raw.lower():
            raw = raw.replace("do", "")
        try:
            price = float(raw.replace("€", "").replace(".", "").replace(",", ".").strip())
        except ValueError as err:
            price = -1.
        return price

    def get_seller(self):
        raw = self.response.xpath("//div[@class='prodajalec']/h2/text()").extract()[0]
        if "zasebna" in raw.lower():
            raw = "ZP"
        return raw

    def get_settlement(self):
        return self.response.xpath("//div[@class='kratek']/strong[@class='rdeca']/text()").extract()[0]

    def get_house_and_land_area(self):
        raw = self.response.xpath("//div[@class='kratek']/text()").extract()[0]
        try:
            house_area = float(raw.split("m2")[0][1:].replace(",", ".").strip())
        except ValueError as err:
            house_area = -1.

        try:
            land_area = int(raw.split("m2")[1].split(",")[-1].replace(".", ""))
        except ValueError as err:
            land_area = -1

        return house_area, land_area

    def get_description(self):
        raw = self.response.xpath("normalize-space(//div[@class='web-opis'])").getall()

        if len(raw) == 0:
            cooked = ""
        elif len(raw) == 1:
            cooked = raw[0]
        else:
            cooked = " ".join(raw)
        cooked = cooked.replace("Dodaten opis", "")

        return cooked
