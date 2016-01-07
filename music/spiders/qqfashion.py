from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from music.items import MusicItem

class QqfashionSpider(CrawlSpider):
    name = 'qqfashion'
    allowed_domains = ['qq.com']
    start_urls = ['http://y.qq.com/y/static/toplist/index/top_7.html?pgv_ref=qqmusic.y.toplist.top_7']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//ol/li')
        
        items = []
        for k in sites:
            i = MusicItem()
            i['rank'] = k.select('span[@class="list_no"]/text()').extract()[0]
            i['name'] = k.select('div[@class = "music_name"]/span/a/@title').extract()[0]
            i['singer'] = k.select('div[@class = "singer_name"]/span/a/text()').extract()[0]
            i['rise'] = k.select('span[@class = "exponent"]/text()').extract()[0]
            #i['num'] = k.select('div[@class="count"]/span/text()').extract()
            items.append(i)
        return items
