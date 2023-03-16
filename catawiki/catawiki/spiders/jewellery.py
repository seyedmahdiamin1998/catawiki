import scrapy
from scrapy.exceptions import CloseSpider
import json

class JewellerySpider(scrapy.Spider):
    name = "jewellery" # !!! Pay attention !!! We use this name as category name of product.
    allowed_domains = ["www.catawiki.com"]
    start_urls = ["https://www.catawiki.com/en/c/313-jewellery"]
    no_page = 1

    def parse(self, response):

        items = response.css("article[class='c-lot-card__container']")
        
        page_ui = response.css('div[id="category-list-page"]::attr(data-props)').extract_first()
        page_ui = json.loads(page_ui)
        initPage = page_ui['initPage']
        initTotalPages = page_ui['initTotalPages']

        if initPage > initTotalPages:
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
        # Product_info
        Product_info = {}
        Product_info['category'] = self.name[:200]

        if not json_data['lotId']:
            Product_info['lotId'] = None
        else:
            Product_info['lotId'] = json_data['lotId']

        if not json_data['lotTitle']:
            Product_info['lotTitle'] = None
        else:
            Product_info['lotTitle'] = json_data['lotTitle'][:50]

        if not json_data['lotSubtitle']:
            Product_info['lotSubtitle'] = None
        else:
            Product_info['lotSubtitle'] = json_data['lotSubtitle'][:50]
        
        if not json_data['description']:
            Product_info['description'] = None
        else:
            Product_info['description'] = json_data['description'][:50]

        if not json_data['auctionId']:
            Product_info['auctionId'] = None
        else:
            Product_info['auctionId'] = json_data['auctionId']
            
        # if not json_data['expertsEstimate']['min']['EUR']:
        if not json_data['expertsEstimate']:
            Product_info['expertsEstimate_min_EUR'] = None
        else:
            Product_info['expertsEstimate_min_EUR'] = json_data['expertsEstimate']['min']['EUR']
        
        # if not json_data['expertsEstimate']['min']['USD']:
        if not json_data['expertsEstimate']:
            Product_info['expertsEstimate_min_USD'] = None
        else:
            Product_info['expertsEstimate_min_USD'] = json_data['expertsEstimate']['min']['USD']
        
        # if not json_data['expertsEstimate']['min']['GBP']:
        if not json_data['expertsEstimate']:
            Product_info['expertsEstimate_min_GBP'] = None
        else:
            Product_info['expertsEstimate_min_GBP'] = json_data['expertsEstimate']['min']['GBP']

        # if not json_data['expertsEstimate']['max']['EUR']:
        if not json_data['expertsEstimate']:
            Product_info['expertsEstimate_max_EUR'] = None
        else:
            Product_info['expertsEstimate_max_EUR'] = json_data['expertsEstimate']['max']['EUR']

        # if not json_data['expertsEstimate']['max']['USD']:
        if not json_data['expertsEstimate']:
            Product_info['expertsEstimate_max_USD'] = None
        else:
            Product_info['expertsEstimate_max_USD'] = json_data['expertsEstimate']['max']['USD']

        # if not json_data['expertsEstimate']['max']['GBP']:
        if not json_data['expertsEstimate']:
            Product_info['expertsEstimate_max_GBP'] = None
        else:
            Product_info['expertsEstimate_max_GBP'] = json_data['expertsEstimate']['max']['GBP']
        
        if not json_data['favoriteCount']:
            Product_info['favoriteCount'] = None
        else:
            Product_info['favoriteCount'] = json_data['favoriteCount']
            
        if not json_data['sellerInfo']['id']:
            Product_info['seller_id'] = None
        else:
            Product_info['seller_id'] = json_data['sellerInfo']['id']

        if not json_data['lotId']:
            Product_info['specification_id'] = None
        else:
            Product_info['specification_id'] = json_data['lotId']
        
        info['Product_info'] = Product_info
        
        # seller_info
        seller_info = {}

        if not json_data['sellerInfo']['id']:
            seller_info['id'] = None
        else:
            seller_info['id'] = json_data['sellerInfo']['id']

        if not json_data['sellerInfo']['userName']:
            seller_info['username'] = None
        else:
            seller_info['username'] = json_data['sellerInfo']['userName'][:50]

        if not json_data['sellerInfo']['address']['country']['name']:
            seller_info['country'] = None
        else:
            seller_info['country'] = json_data['sellerInfo']['address']['country']['name'][:50]

        if not json_data['sellerInfo']['address']['city']:
            seller_info['city'] = None
        else:
            seller_info['city'] = json_data['sellerInfo']['address']['city'][:50]

        if not json_data['sellerInfo']['address']['state'] : 
            seller_info['state'] = None
        else:
            seller_info['state'] = json_data['sellerInfo']['address']['state'][:50]
        
        if not json_data['sellerInfo']['address']['zipcode']:
            seller_info['zipcode']= None 
        else:
            seller_info['zipcode'] = json_data['sellerInfo']['address']['zipcode'][:50]
            
        if not json_data['sellerInfo']['isPro']:
            seller_info['isPro'] = None
        else:
            seller_info['isPro'] = json_data['sellerInfo']['isPro']
        
        if not json_data['sellerInfo']['isTop']:
            seller_info['isTop'] = None
        else:
            seller_info['isTop'] = json_data['sellerInfo']['isTop'] 
        
        if not json_data['sellerInfo']['createdAt']:
            seller_info['createdAt'] = None
        else:
            seller_info['createdAt'] = json_data['sellerInfo']['createdAt'][:50]

        if not json_data['sellerInfo']['url']:
            seller_info['url'] = None
        else:
            seller_info['url'] = json_data['sellerInfo']['url'][:200]      
            
        info['seller_info'] = seller_info

        # specification_info
        specification_info = {}
        if not json_data['lotId']:
            specification_info['specification_id'] = None
        else:    
            specification_info['specification_id'] = json_data['lotId']

        if not json_data['specifications']:
            specification_info['specification_items'] = [{'lotId':specification_info['specification_id'], 'name':None, 'value': None}]     
        else:
            specification_info['specification_items'] = [{'lotId':specification_info['specification_id'], 'name':item['name'][:200], 'value':item['value'][:1000]} for item in json_data['specifications']]
        info['specification_info'] = specification_info

        # feedbacks_info
        feedbacks_info = {}
        if not json_data['lotId']:
            feedbacks_info['feeedback_id'] = None
        else:
            feedbacks_info['feeedback_id'] = json_data['lotId']
        
        if not json_data['feedbacks']:
            feedbacks_info['feedbacks_items'] = [{  'lotId':feedbacks_info['feeedback_id'],
                                                    'type':None,
                                                    'authorName':None,
                                                    'body':None,
                                                    'locale':None,
                                                    'createdAt':None}]
        else:
            feedbacks_info['feedbacks_items'] = [{  'lotId':feedbacks_info['feeedback_id'],
                                                    'type':item['type'][:50],
                                                    'authorName':item['authorName'],
                                                    'body':item['body'][:2000],
                                                    'locale':item['locale'][:50],
                                                    'createdAt':item['createdAt'][:50]} for item in json_data['feedbacks']]

        info['feedbacks_info'] = feedbacks_info
        yield info

