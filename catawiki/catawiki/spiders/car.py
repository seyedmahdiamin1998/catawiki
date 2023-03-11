import scrapy
from scrapy.exceptions import CloseSpider
import json

class CarSpider(scrapy.Spider):
    name = "car"
    allowed_domains = ["www.catawiki.com"]
    start_urls = ["https://www.catawiki.com/en/c/423-classic-cars"]
    no_page = 15

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
        info['lotId'] = json_data['lotId']
        info['lotTitle'] = json_data['lotTitle']
        info['lotSubtitle'] = json_data['lotSubtitle']
        info['description'] = json_data['description']
        
        
        info['auctionId'] = json_data['auctionId']

        info['expertsEstimate_min_EUR'] = json_data['expertsEstimate']['min']['EUR']
        info['expertsEstimate_min_USD'] = json_data['expertsEstimate']['min']['USD']
        info['expertsEstimate_min_GBP'] = json_data['expertsEstimate']['min']['GBP']
        info['expertsEstimate_max_EUR'] = json_data['expertsEstimate']['max']['EUR']
        info['expertsEstimate_max_USD'] = json_data['expertsEstimate']['max']['USD']
        info['expertsEstimate_max_GBP'] = json_data['expertsEstimate']['max']['GBP']
        
        info['favoriteCount'] = json_data['favoriteCount']

        yield info
        
       



# response.css("div[data-react-component='LotDetailsPage']::attr(data-props)").extract_first()


# response.xpath('//div[has-class("lot-details-page-wrappe")]')

# scrapy crawl car -o a.json