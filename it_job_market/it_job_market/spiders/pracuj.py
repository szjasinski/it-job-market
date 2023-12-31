import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from it_job_market.items import ItJobMarketItem
from datetime import datetime


# CLASS FOR SCRAPING PRACUJ.PL JOB OFFERS
PRACUJ_PAGES_NUM = 2
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
        item["min_salary"] = response.xpath('//span[@data-test="text-earningAmountValueFrom"]/text()').get()
        item["max_salary"] = response.xpath('//span[@data-test="text-earningAmountValueTo"]/text()').get()
        item["price_unit"] = response.xpath('//span[@data-test="text-earningAmountUnit"]/text()').get()
        item["contract_type"] = response.xpath('//div[@data-test="sections-benefit-contracts-text"]/text()').get()
        item["city"] = response.xpath('//div[@data-scroll-id="workplaces"]/div/div[@data-test="text-benefit"]/text()').get()
        item["expiration_date"] = response.xpath('//div[@data-scroll-id="publication-dates"]/div/div[2]/text()').get()
        item["work_schedule"] = response.xpath('//div[@data-test="sections-benefit-work-schedule"]/div/div/text()').get()
        item["position_level"] = response.xpath(
            '//div[@data-test="sections-benefit-employment-type-name"]/div/div/text()').get()
        item["work_mode"] = response.xpath(
            '//div[@data-test="sections-benefit-work-modes"]/div/div/text()').get()
        item["specialization"] = response.xpath(
            '//li[@data-test="it-specializations"]/span[2]/text()').get()

        item["expected_technologies"] = response.xpath(
            '//div[@data-test="section-technologies-expected"]/ul/li/p/text()').getall()
        item["optional_technologies"] = response.xpath(
            '//div[@data-test="section-technologies-optional"]/ul/li/p/text()').getall()
        item["about_project"] = response.xpath('//div[@data-test="text-about-project"]/p/text()').get()
        item["responsibilities"] = response.xpath(
            '//div[@data-test="section-responsibilities"]/ul/li/p/text()').getall()
        item["expected_requirements"] = response.xpath(
            '//div[@data-test="section-requirements-expected"]/ul/li/p/text()').getall()
        item["optional_requirements"] = response.xpath(
            '//div[@data-test="section-requirements-optional"]/ul/li/p/text()').getall()
        item["development_opportunities"] = response.xpath(
            '//div[@data-test="section-training-space"]/div/ul/li/p/text()').getall()
        item["what_they_offer"] = response.xpath(
            '//div[@data-test="section-offered"]/div/ul/li/p/text()').getall()
        item["benefits"] = response.xpath(
            '//section[@data-test="section-benefits"]/ul/li/article/p/text()').getall()

        item["url"] = response.url
        item["source"] = "pracuj.pl"
        item["scraping_datetime"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        direct_address = response.xpath('//div[@data-scroll-id="workplaces"]/div/a/text()').get()
        if direct_address:
            item["address"] = direct_address
        else:
            general_address = response.xpath('//div[@data-scroll-id="workplaces"]/div/p/text()').get()
            item["address"] = general_address

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
