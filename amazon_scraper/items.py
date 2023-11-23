import scrapy


class AmazonScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AmazonSearchItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    avg_rating = scrapy.Field()
    total_review = scrapy.Field()
    image = scrapy.Field()
    
class AmazonReviewItem(scrapy.Item):
    asin = scrapy.Field()
    text = scrapy.Field()
    title = scrapy.Field()
    verified = scrapy.Field()
    rating = scrapy.Field()
    location_and_date = scrapy.Field()
    
class AmazonCategoryItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    avg_rating = scrapy.Field()
    total_review = scrapy.Field()
    image = scrapy.Field()