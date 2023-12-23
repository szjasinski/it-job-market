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
    source = scrapy.Field()
    scraping_datetime = scrapy.Field()
    work_schedule = scrapy.Field()
    position_level = scrapy.Field()
    work_mode = scrapy.Field()
    specialization = scrapy.Field()
    expected_technologies = scrapy.Field()
    optional_technologies = scrapy.Field()
    about_project = scrapy.Field()
    responsibilities = scrapy.Field()
    expected_requirements = scrapy.Field()
    optional_requirements = scrapy.Field()
    development_opportunities = scrapy.Field()
    what_they_offer = scrapy.Field()
    benefits = scrapy.Field()