import scrapy
from scrapy.exceptions import CloseSpider
import json

class CarSpider(scrapy.Spider):
    name = "car" # !!! Pay attention !!! We use this name as category name of product.
    allowed_domains = ["www.catawiki.com"]
    start_urls = ["https://www.catawiki.com/en/c/423-classic-cars"]
    no_page = 2

    def parse(self, response):

        items = response.css("article[class='c-lot-card__container']")
        
        if len(items)<1:
            raise CloseSpider('Finish')
        
        for item in items:
            detail_page_url = item.css('a::attr(href)').extract_first() 
            yield scrapy.Request(url = detail_page_url, callback = self.parse_detail)

        next_page_url = response.urljoin(f"?page={self.no_page}") 
        self.no_page = self.no_page + 1
        yield scrapy.Request(url = next_page_url , callback = self.parse)

    def parse_detail(self, response):
        json_data = response.css("div[data-react-component='LotDetailsPage']::attr(data-props)").extract_first()
        json_data = json.loads(json_data)

        info = {}

        seller_info = {}
        seller_info['id'] = json_data['sellerInfo']['id']
        seller_info['username'] = json_data['sellerInfo']['userName']
        seller_info['country'] = json_data['sellerInfo']['address']['country']['name']
        seller_info['city'] = json_data['sellerInfo']['address']['city']
        if not json_data['sellerInfo']['address']['state'] : 
            seller_info['state'] = ''
        else:
            seller_info['state'] = json_data['sellerInfo']['address']['state'] 
        seller_info['zipcode'] = json_data['sellerInfo']['address']['zipcode'] 
        seller_info['isPro'] = json_data['sellerInfo']['isPro'] 
        seller_info['isTop'] = json_data['sellerInfo']['isTop'] 
        seller_info['createdAt'] = json_data['sellerInfo']['createdAt'] 
        seller_info['url'] = json_data['sellerInfo']['url']         
        info['seller_info'] = seller_info

        Product_info = {}
        Product_info['lotId'] = json_data['lotId']
        Product_info['category'] = self.name
        Product_info['lotTitle'] = json_data['lotTitle']
        Product_info['lotSubtitle'] = json_data['lotSubtitle']
        Product_info['description'] = json_data['description']
        Product_info['auctionId'] = json_data['auctionId']
        Product_info['expertsEstimate_min_EUR'] = json_data['expertsEstimate']['min']['EUR']
        Product_info['expertsEstimate_min_USD'] = json_data['expertsEstimate']['min']['USD']
        Product_info['expertsEstimate_min_GBP'] = json_data['expertsEstimate']['min']['GBP']
        Product_info['expertsEstimate_max_EUR'] = json_data['expertsEstimate']['max']['EUR']
        Product_info['expertsEstimate_max_USD'] = json_data['expertsEstimate']['max']['USD']
        Product_info['expertsEstimate_max_GBP'] = json_data['expertsEstimate']['max']['GBP']
        Product_info['favoriteCount'] = json_data['favoriteCount']
        Product_info['seller_id'] = json_data['sellerInfo']['id']

        info['Product_info'] = Product_info

        yield info