# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ItJobMarketItem(scrapy.Item):

    job_title = scrapy.Field()
    employer = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    price_unit = scrapy.Field()
    url = scrapy.Field()
    contract_type = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    expiration_date = scrapy.Field()
    logo_url = scrapy.Field()
    source = scrapy.Field()
    scraping_datetime = scrapy.Field()

