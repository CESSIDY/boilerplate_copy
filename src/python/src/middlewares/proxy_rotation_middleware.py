from scrapy import Spider, Request, Spider, signals
import logging
from datetime import datetime, timedelta
import random
import json
from w3lib.http import basic_auth_header

log = logging.getLogger('scrapy.proxy_rotation')

class Mode:
    RANDOMIZE_EVERY_REQUESTS, IN_ORDER_EVERY_REQUESTS = range(1,3) # 1, 2

class ProxyRotationMiddleware:
    logging_enabled = True

    def __init__(self, settings) -> None:
        self.proxy_list: list = json.loads(settings['PROXY_LIST']) if settings['PROXY_LIST'] else None
        self.mode: int = int(settings['PROXY_MODE']) if settings['PROXY_MODE'] else None
        self.proxy: str = settings['PROXY']
        self.proxy_auth: str = settings['PROXY_AUTH']
        self.proxy_enabled: bool = bool(settings['PROXY_ENABLED']) if settings['PROXY_ENABLED'] else None

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider: Spider):
        self.mode = getattr(spider, 'proxy_mode', self.mode)
        self.proxy_enabled = getattr(spider, 'proxy_enabled', self.proxy_enabled)

    def process_request(self, request: Request, spider: Spider) -> None:
        if self.proxy_enabled:
            request = self.update_request(request, spider)
        else:
            if self.logging_enabled:
                spider.logger.warning('PROXY DISABLED')
                self.logging_enabled = False

    def update_request(self, request: Request, spider: Spider) -> Request:
        if self.proxy_list:
            proxy_item = None

            if self.mode == Mode.RANDOMIZE_EVERY_REQUESTS:
                proxy_item = random.choice(list(self.proxy_list))
            elif self.mode == Mode.IN_ORDER_EVERY_REQUESTS:
                proxy_item = self.proxy_list.pop(0)
                self.proxy_list.append(proxy_item)
            else:
                raise Exception(f"PROXY_MODE is {self.mode}, need to be 1 or 2")

            if proxy_item and proxy_item.get("proxy"):
                proxy = proxy_item.get("proxy")
                proxy_auth = proxy_item.get("auth")
                if proxy_auth:
                    request.headers["Proxy-Authorization"] = basic_auth_header(*proxy_auth.split(":"))
                if "http" not in proxy:
                    proxy = "http://{}".format(proxy)
                request.meta["proxy"] = proxy
                return request
            else:
                raise Exception(f"Proxy ({self.proxy_list.index(proxy_item)}) from list is empty")
