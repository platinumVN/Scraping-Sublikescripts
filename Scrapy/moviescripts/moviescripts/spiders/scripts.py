import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ScriptsSpider(CrawlSpider):
    name = 'scripts'
    allowed_domains = ['subslikescript.com']
    # start_urls = ['https://subslikescript.com/movies'] # https target website
    # start_urls = ['https://subslikescript.com/movies_letter-T']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63'
    def start_requests(self):
        yield scrapy.Request(url='https://subslikescript.com/movies_letter-X', headers={
            'user-agent' : self.user_agent
        })

    rules = (
        # Extract all movie script's page links from the movies page:
        Rule(
            LinkExtractor(restrict_xpaths=('//ul[@class="scripts-list"]/a')), # path to a list of element containing target links
            callback= 'parse_item', # pass function name as a string
            follow=True,
            process_request='set_user_agent'
        ),
        # Get (go to) the next page (after finish the first Rule)
        Rule(
            LinkExtractor(restrict_xpaths=('(//a[@rel="next"])[1]'))
        ),
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        article = response.xpath('//article[@class="main-article"]')
        # print(response.url) # print extracted links
        transcript_list = article.xpath('./div[@class="full-script"]/text()').getall()
        transcript_string = ' '.join(transcript_list)
        yield {
            'title' : article.xpath('./h1/text()').get(),
            'plot' : article.xpath('./p/text()').get(),
            'script' : transcript_string,
            'url' : response.url,
            'user_agent' : response.request.headers['User-Agent']
        }
