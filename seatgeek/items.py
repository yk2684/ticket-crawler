# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SeatgeekItem(scrapy.Item):
    # define the fields for your item here like:
    #name = scrapy.Field()
    performance = scrapy.Field()
    currentPrice = scrapy.Field()
    listingId = scrapy.Field()
    quantity = scrapy.Field()
    row = scrapy.Field()
    seatNumbers = scrapy.Field()
    sectionName = scrapy.Field()
    zoneName = scrapy.Field()
    eventId = scrapy.Field()
    vendor = scrapy.Field()
    listingPrice = scrapy.Field()
    datePulled = scrapy.Field()
    location = scrapy.Field()