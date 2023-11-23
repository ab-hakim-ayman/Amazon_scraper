import scrapy
from urllib.parse import urljoin
from amazon_scraper.items import AmazonReviewItem
from amazon_scraper.itemloaders import AmazonReviewLoader


class AmazonReviewSpider(scrapy.Spider):
    name = "amazon_review"
    allowed_domains = ["www.amazon.com"]
    start_urls = ["https://www.amazon.com/"]
    api_key = 'f08e2190b42cfd5e5ea26d582d340d2c'
    base_url = 'http://api.scraperapi.com'
    
    custom_settings = {
        'FEEDS' : { 'data/%(name)s_%(time)s.csv' : { 'format':'csv' }}
    }
    
    def start_requests(self):
        asin_list = ['B09G9FPHY6','B09G9CJM1Z','B0BJLFC67L','B09G91LXFP','B0BJLF2BRM']
        for asin in asin_list:
            url = f'https://www.amazon.com/product-reviews/{asin}/'       
            proxy_url = f'{self.base_url}/?api_key={self.api_key}&url={url}'
            yield scrapy.Request(url=proxy_url, callback=self.parse_reviews, meta={'asin': asin})
        

    def parse_reviews(self, response):
        asin = response.meta['asin']
        reviews = response.css("#cm_cr-review_list div[data-hook='review']")
        for review in reviews:       
            text = "".join(review.css("span[data-hook=review-body] ::text").getall()).strip()
            title = review.css("*[data-hook=review-title]>span::text").get()
            location_and_date = review.css("span[data-hook=review-date] ::text").get()
            verified = bool(review.css("span[data-hook=avp-badge] ::text").get())
            rating = review.css("*[data-hook*=review-star-rating] ::text").re(r"(\d+\.*\d*) out")[0]
            
            loader = AmazonReviewLoader(item=AmazonReviewItem(), selector=review)
            loader.add_value('asin', asin)
            loader.add_value('text', text)
            loader.add_value('title', title)
            loader.add_value('rating', rating)
            loader.add_value('verified', verified)
            loader.add_value('location_and_date', location_and_date)
            item = loader.load_item()
            self.log(f"Scraped item: {item}")
            yield item

        next_page_relative_url = response.css(".a-pagination .a-last>a::attr(href)").get()
        if next_page_relative_url is not None:
            next_url = f'https://www.amazon.com/{next_page_relative_url}'
            proxy_url = f'{self.base_url}/?api_key={self.api_key}&url={next_url}'
            yield scrapy.Request(url=proxy_url, callback=self.parse_reviews, dont_filter=True, meta={'asin': asin})
