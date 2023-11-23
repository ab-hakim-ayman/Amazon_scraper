from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class AmazonScraperPipeline:
    def process_item(self, item, spider):
        return item

class DuplicatesPipeline:
    def __init__(self):
        self.titles_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['title'] in self.titles_seen:
            raise DropItem(f"Duplicate item found: {item}")
        else:
            self.titles_seen.add(adapter['title'])
            return item
        
class MySQLPipeline(object):

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.con = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '12345678',
            database = 'amazon'
        )
        self.cur = self.con.cursor()
        
    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.cur.execute(""" insert into chocolate ( title, price, avg_rating, total_review, image)  values (%s,%s,%s,%s,%s)""", (
            item["title"],
            item["price"],
            item["avg_rating"],
            item["total_review"],
            item["image"],
        ))
        self.con.commit()