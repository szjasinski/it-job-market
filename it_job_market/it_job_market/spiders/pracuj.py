import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from it_job_market.items import ItJobMarketItem


# CLASS FOR SCRAPING PRACUJ.PL JOB OFFERS
PRACUJ_PAGES_NUM = 3
pracuj_urls_generator = ["https://it.pracuj.pl/praca?pn=" + str(i) for i in range(1, PRACUJ_PAGES_NUM + 1)]


class PracujSpider(CrawlSpider):

    name = "pracuj"
    allowed_domains = ["pracuj.pl"]
    start_urls = pracuj_urls_generator

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
        item["city"] = response.xpath('//div[@data-scroll-id="workplaces"]/div/div[@data-test="text-benefit"]/text()').get()
        item["expiration_date"] = response.xpath('//div[@data-scroll-id="publication-dates"]/div/div[2]/text()').get()
        item["url"] = response.url
        item["source"] = "pracuj.pl"

        direct_address = response.xpath('//div[@data-scroll-id="workplaces"]/div/a/text()').get()
        if direct_address:
            item["address"] = direct_address
        else:
            approximate_address = response.xpath('//div[@data-scroll-id="workplaces"]/div/p/text()').get()
            item["address"] = approximate_address

        # doesnt work -> logo is loaded after a short delay
        # logo_url = response.xpath('//img[@data-test="section-company-logo"]/@src').get()

        return item


# # CLASS FOR SCRAPING NOFLUFFJOBS JOB OFFERS
# nofluff_pages_num = 1
# SEARCH_STR = "https://nofluffjobs.com/backend?criteria=category%3Dfrontend,fullstack,mobile,embedded,testing,devops," \
#              "architecture,security,gaming,artificial-intelligence,big-data,it-administrator,agile," \
#              "product-management,project-manager,business-intelligence,business-analyst,ux,support,erp&page="
# nofluff_urls_generator = [SEARCH_STR + str(i) for i in range(1, nofluff_pages_num + 1)]
#
#
# class NoFluffSpider(CrawlSpider):
#
#     name = "nofluff"
#     allowed_domains = ["nofluffjobs.com"]
#     start_urls = nofluff_urls_generator
#
#     rules = (
#         Rule(LinkExtractor(allow=(r".*/job/.*",)), callback="parse_item"),
#     )
#
#     def parse_item(self, response):
#         item = ItJobMarketItem()
#         item["job_title"] = response.xpath('//h1[@class="font-weight-bold bigger"]/text()').get()
#
#         # employer doesnt work
#         item["employer"] = response.xpath('//a[@data-cy="JobOffer_CompanyProfile"]/text()').get()
#
#         item["source"] = "nofluffjobs.com"
#
#         return item


# # CLASS FOR SCRAPING JUSTJOINIT JOB OFFERS
# justjoin_pages_num = 1
# justjoin_urls_generator = ["XXX" + str(i) for i in range(1, justjoin_pages_num+1)]
#
#
# class JustJoinSpider(CrawlSpider):
#
#     name = "justjoin"
#     allowed_domains = ["justjoin.it"]
#     start_urls = nofluff_urls_generator
#
#     rules = (
#         Rule(LinkExtractor(allow=(r"XXX",)), callback="parse_item"),
#     )
#
#     def parse_item(self, response):
#         item = ItJobMarketItem()
#
#         item["source"] = "justjoin.it"
#
#         return item
