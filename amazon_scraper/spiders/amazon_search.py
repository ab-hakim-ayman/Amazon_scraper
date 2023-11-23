import scrapy
from urllib.parse import urljoin
from amazon_scraper.items import AmazonSearchItem
from amazon_scraper.itemloaders import AmazonSearchLoader


class AmazonSearchSpider(scrapy.Spider):
    name = "amazon_search"
    allowed_domains = ["www.amazon.com"]
    start_urls = ["https://www.amazon.com/"]
    api_key = 'f08e2190b42cfd5e5ea26d582d340d2c'
    base_url = 'http://api.scraperapi.com'
    
    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv'}}
    }
    
    def start_requests(self):
        keyword_list = ['ipad']
        for keyword in keyword_list:
            url = f'https://www.amazon.com/s?k={keyword}&page=1'
            proxy_url = f'{self.base_url}/?api_key={self.api_key}&url={url}'
            yield scrapy.Request(url=proxy_url, callback=self.discover_product_urls, meta={'keyword': keyword, 'page': 1})

    def discover_product_urls(self, response):
        page = response.meta['page']
        keyword = response.meta['keyword'] 

        products = response.css("div.s-result-item[data-component-type=s-search-result]")
        for product in products:
            relative_url = product.css("h2>a::attr(href)").get()
            product_url = urljoin('https://www.amazon.com/', relative_url).split("?")[0]
            yield scrapy.Request(url=product_url, callback=self.parse_product_data, meta={'keyword': keyword, 'page': page})
            
        if page == 1:
            available_pages = response.xpath(
                '//*[contains(@class, "s-pagination-item")][not(has-class("s-pagination-separator"))]/text()'
            ).getall()

            last_page = available_pages[-1]
            for p in range(2, int(last_page)):
                url = f'https://www.amazon.com/s?k={keyword}&page={p}'
                proxy_url = f'{self.base_url}/?api_key={self.api_key}&url={url}'
                yield scrapy.Request(url=proxy_url, callback=self.discover_product_urls, dont_filter=True, meta={'keyword': keyword, 'page': p})

    def parse_product_data(self, response):
        if response.status == 200:
            title = response.css('h1 span#productTitle::text').get()
            price = response.css('.a-price span.a-offscreen::text').get()
            if not price:
                price = response.css('.a-price span[aria-hidden="true"] span.a-price-whole::text').get()
            loader = AmazonSearchLoader(item=AmazonSearchItem(), response=response)
            loader.add_value('title', title.strip() if title else None)
            loader.add_value('price', price)
            loader.add_css('avg_rating', 'span[data-hook="rating-out-of-text"]::text')
            loader.add_css('total_review', 'div span[data-hook="total-review-count"]::text')
            loader.add_css('image', 'div#imgTagWrapperId img::attr(src)')

            item = loader.load_item()
            self.log(f"Scraped item: {item}")
            yield item
            
        else:
            self.log(f"Unexpected status code: {response.status}")