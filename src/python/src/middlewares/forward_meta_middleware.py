from scrapy import Spider, Request, Spider, signals
import logging

class ForwardMetaMiddleware:
    """This middleware allows spiders to use the user_agent from list"""

    def __init__(self):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings['USER_AGENT'])
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider: Spider):
        pass

    def process_request(self, request: Request, spider: Spider):
        pass
