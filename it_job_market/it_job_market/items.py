# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ItJobMarketItem(scrapy.Item):

    job_title = scrapy.Field()
    employer = scrapy.Field()
    price_from = scrapy.Field()
    price_to = scrapy.Field()
    price_unit = scrapy.Field()
    url = scrapy.Field()
    contract_type = scrapy.Field()
