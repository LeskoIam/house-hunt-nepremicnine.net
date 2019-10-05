from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from .constants import URL, DOMAIN
from ..items import HousehuntItem


class ExampleSpider(CrawlSpider):
    name = 'nepremicnine'
    allowed_domains = [DOMAIN]
    start_urls = [URL]

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[contains(@class, 'oglas_container')]/div/a[contains(@href, 'oglasi-prodaja')]"),
             callback="parse_single_listing"),
        # Crawl "next" pages
        Rule(LinkExtractor(restrict_xpaths="(//div[@id='pagination']/ul/li[@class='paging_next']/a[@class='next'])[1]")),
    )

    def parse_single_listing(self, response):
        item = HousehuntItem()

        _, type_, regija, upravna_enota, obcina = self.get_basic_info(response)

        item["type_"] = type_
        item["region"] = regija
        item["administrative_unit"] = upravna_enota
        item["municipality"] = obcina
        item["url"] = response.url
        item["price"] = self.get_price(response)
        item["seller"] = self.get_seller(response)
        item["settlement"] = self.get_settlement(response)

        yield item

    @staticmethod
    def get_basic_info(response):
        """
        Vrsta
        Regija
        Upravna enota
        Obcina
        """

        raw = response.xpath("//div[@class='more_info'][contains(.,'Posredovanje')]/text()").extract()

        raw = raw[0].split("|")
        out = []
        for data in raw:
            data = data.split(":")[-1].strip()
            out.append(data)
        return out

    @staticmethod
    def get_price(response):
        raw = response.xpath("//div[@class='cena clearfix']/span/text()").extract()[0]
        if "cca" in raw.lower():
            raw = raw.replace("cca", "")
        if "do" in raw.lower():
            raw = raw.replace("do", "")
        try:
            price = float(raw.replace("€", "").replace(".", "").replace(",", ".").strip())
        except Exception as exc:
            price = -1.
        return price

    @staticmethod
    def get_seller(response):
        raw = response.xpath("//div[@class='prodajalec']/h2/text()").extract()[0]
        if "zasebna" in raw.lower():
            raw = "ZP"
        return raw

    @staticmethod
    def get_settlement(response):
        return response.xpath("//div[@class='kratek']/strong[@class='rdeca']/text()").extract()[0]

