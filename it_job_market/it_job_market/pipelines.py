# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import sqlite3


class WhitespacesPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        for key, value in adapter.items():
            val = str(value)
            adapter[key] = val.strip()
        return item


class CleanPricePipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        for field in ["price_from", "price_to"]:
            val = str(adapter.get(field))
            adapter[field] = val.replace('\xa0', '').replace(',00', '')
        return item


#
class WithPricePipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("price_from") and adapter.get("price_to"):
            return item
        else:
            raise DropItem(f"Missing price data in {item}")


class ToMonthlyPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        hourly_units = ["brutto / godz.",
                        "net (+ VAT) / hr.",
                        "netto (+ VAT) / godz.",
                        "gross / hr.", ]

        monthly_units = ["brutto / mies.",
                         "net (+ VAT) / mth.",
                         "netto (+ VAT) / mies.",
                         "netto (+ VAT) / mies.", ]

        if adapter.get("price_unit") in hourly_units:
            adapter["price_from"] = int(adapter.get("price_from")) * 160
            adapter["price_to"] = int(adapter.get("price_to")) * 160
            adapter["price_unit"] = "gross / mth."

        if adapter.get("price_unit") in monthly_units:
            adapter["price_unit"] = "gross / mth."

        return item


class SqlitePipeline:

    def __init__(self):
        # Create/Connect to database
        self.con = sqlite3.connect('it-job-market.db')

        # Create cursor, used to execute commands
        self.cur = self.con.cursor()

        # Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS offers(
            job_title TEXT,
            employer TEXT,
            price_from TEXT,
            price_to TEXT,
            price_unit TEXT,
            url TEXT,
            contract_type TEXT
        )
        """)

    def process_item(self, item, spider):
        # Define insert statement
        self.cur.execute("""INSERT INTO offers (job_title, employer, price_from, price_to, price_unit, url, 
        contract_type) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                         (
                             item['job_title'],
                             item['employer'],
                             item['price_from'],
                             item['price_to'],
                             item['price_unit'],
                             item['url'],
                             item['contract_type']
                             
                         ))

        # Execute insert of data into database
        self.con.commit()
        return item

