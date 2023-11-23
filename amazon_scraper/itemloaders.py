from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose


class AmazonSearchLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    price_in = MapCompose(lambda x: x.split('$')[-1])
    avg_rating_in = MapCompose(lambda x: x.split(' ')[0])
    total_review_in = MapCompose(lambda x: x.split(' ')[0])
    
class AmazonReviewLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    text_in = MapCompose(lambda x: ' '.join(x.split()[:25]))
    
class AmazonCategoryLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    price_in = MapCompose(lambda x: x.split('$')[-1])
    avg_rating_in = MapCompose(lambda x: x.split(' ')[0])
    total_review_in = MapCompose(lambda x: x.split(' ')[0])