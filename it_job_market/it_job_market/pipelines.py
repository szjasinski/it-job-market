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


class CleanContractPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        b2b_contracts = ["B2B contract", "kontrakt B2B"]
        employment_contracts = ["contract of employment", "umowa o pracę", ]
        mandate_contracts = ["umowa zlecenie"]

        item_contract_data = str(adapter.get("contract_type"))
        item_contracts = item_contract_data.split(", ")

        contract_string = ''

        for c in item_contracts:
            if c in b2b_contracts:
                if len(contract_string) == 0:
                    contract_string = 'B2B'
                else:
                    contract_string += ', B2B'
            elif c in employment_contracts:
                if len(contract_string) == 0:
                    contract_string = 'employment'
                else:
                    contract_string += ', employment'
            elif c in mandate_contracts:
                if len(contract_string) == 0:
                    contract_string = 'mandate'
                else:
                    contract_string += ', mandate'

        adapter['contract_type'] = contract_string
        return item


class CleanDatePipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        val = str(adapter.get('expiration_date'))
        date_to_clean = val.replace("do: ", '').replace("until: ", '')

        month_dict = {'sty': '01', 'lut': '02', 'mar': '03', 'kwi': '04', 'maj': '05', 'cze': '06',
                      'lip': '07', 'sie': '08', 'wrz': '09', 'paź': '10', 'lis': '11', 'gru': '12',
                      'jan': '01', 'feb': '02', 'MAR': '03', 'apr': '04', 'may': '05', 'jun': '06',
                      'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12',
                      }
        date_parts = date_to_clean.split()
        new_format_month = month_dict[date_parts[1].lower()]
        date_parts[1] = new_format_month
        adapter['expiration_date'] = "-".join(date_parts)

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
            price_from INT,
            price_to INT,
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
