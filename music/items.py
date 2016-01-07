# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class MusicItem(Item):
    rank = Field()
    name = Field()
    singer = Field()
    num = Field()
    comments = Field()
    days = Field()
    change = Field()
    changedays = Field()
    rise = Field()
    share = Field()
