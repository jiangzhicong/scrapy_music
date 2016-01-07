from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from music.items import MusicItem
from scrapy.item import Item
from scrapy.http import Request

class A163newSpider(CrawlSpider):
    name = '163new'
    allowed_domains = ['163.com']
    start_urls = ['http://music.163.com/discover/toplist?id=3779629']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse(self, response): 
        hxs=HtmlXPathSelector(response)
        sites = hxs.select('//tbody/tr')
        
        p = 0
        for k in sites:
            
            p += 1
            i = MusicItem()
            
            i['rank'] = int(k.select('td/div/span[contains(@class,"num")]/text()').extract()[0])
            if p < 4:
                url = k.select('td/div/div/div/span[@class="txt"]/strong/a/@href').extract()[0]
                i['name'] = k.select('td/div/div/div/span/strong/@title').extract()[0].split('(')[0].split('[')[0].split('\u3010')[0].split('<')[0]
            else:
                url = k.select('td/div/div/div/span[@class="txt"]/b/a/@href').extract()[0]
                i['name'] = k.select('td/div/div/div/span/b/@title').extract()[0].split('(')[0].split('[')[0].split('\u3010')[0].split('<')[0]
                
            i['singer'] = k.select('td/div[@class="text"]/span/@title').extract()[0]

            yield Request("http://music.163.com"+url, meta = {'rank':i['rank'],'name':i['name'],'singer':i['singer']}, callback=self.parse_item)

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = MusicItem()
        
        i['comments'] = long(hxs.select('//span[@id="cnt_comment_count"]/text()').extract()[0])
        i['rank'] = response.meta['rank']
        i['name'] = response.meta['name']
        i['singer'] = response.meta['singer']
        
        return i
