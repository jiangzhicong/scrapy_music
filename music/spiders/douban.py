from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from music.items import MusicItem

class DoubanSpider(CrawlSpider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['http://music.douban.com/chart']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//ul[@class = "col5"]/li')
        items = []
        idex = 0
        for k in sites:
            idex += 1
            i = MusicItem()
            i['rank'] = int(k.select('span[@class = "green-num-box"]/text()').extract()[0])
            i['name'] = k.select('div/h3/a/text()|div/p/a/text()').extract()[0].split('(')[0].split('[')[0].split('<')[0]

            if idex < 11:
                a = k.select('div/p/text()').extract()[0]
                i['singer'] = a.split('/')[0][:-1]
                i['num'] = int(a.split('/')[1][1:-3])
            else:
                a = k.select('div/p/text()').extract()[1]
                i['singer'] = a.split('/')[0][17:-1]
                i['num'] = int(a.split('/')[1][1:-16])

            i['days'] = int(k.select('span[@class = "days"]/text()').extract()[0][3:-2])

            b = k.select('span[contains(@class, "trend")]/@class').extract()[0][-1]
            if b == "p":i['change'] = "up"
            elif b == "n":i['change'] = "down"
            else: i['change'] = "no"
        
            i['changedays'] = int(k.select('span[contains(@class,"trend")]/text()').extract()[0][1])
            items.append(i)

        return items
