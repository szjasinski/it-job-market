import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from it_job_market.items import ItJobMarketItem


# CLASS FOR SCRAPING PRACUJ.PL JOB OFFERS
urls_generator = ["https://it.pracuj.pl/praca?pn=" + str(i) for i in range(1,2)]


class PracujSpider(CrawlSpider):

    name = "pracuj"
    allowed_domains = ["pracuj.pl"]
    start_urls = urls_generator

    rules = (
        Rule(LinkExtractor(allow=(r"praca/.*,oferta,.*",)), callback="parse_item"),
    )

    def parse_item(self, response):
        item = ItJobMarketItem()
        item["job_title"] = response.xpath('//h1[@data-scroll-id="job-title"]/text()').get()
        item["employer"] = response.xpath('//h2[@data-scroll-id="employer-name"]/text()').get()
        item["price_from"] = response.xpath('//span[@data-test="text-earningAmountValueFrom"]/text()').get()
        item["price_to"] = response.xpath('//span[@data-test="text-earningAmountValueTo"]/text()').get()
        item["price_unit"] = response.xpath('//span[@data-test="text-earningAmountUnit"]/text()').get()
        item["contract_type"] = response.xpath('//div[@data-test="sections-benefit-contracts-text"]/text()').get()

        item["url"] = response.url

        return item
