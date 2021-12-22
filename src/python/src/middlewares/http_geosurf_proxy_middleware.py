# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from w3lib.http import basic_auth_header
import random

class HttpGeosurfProxyMiddleware:
    logging_enabled = True

    @staticmethod
    def update_request(request: Request, spider: Spider) -> Request:
        random_number = random.randrange(100_000, 999_999)
        proxy = "us-1m.geosurf.io:8000"
        proxy_auth = f"601743+US+601743-{random_number}:5938a5880"
        spider.logger.info(proxy)
        spider.logger.info(proxy_auth)

        if not proxy:
            raise Exception('Proxy enabled but not configured')

        if proxy_auth:
            request.headers["Proxy-Authorization"] = basic_auth_header(*proxy_auth.split(":"))
        if "http" not in proxy:
            proxy = "http://{}".format(proxy)
        request.meta["proxy"] = proxy
        return request

    def process_request(self, request: Request, spider: Spider) -> None:
        if hasattr(spider, "proxy_enabled") and spider.proxy_enabled or spider.settings.get("PROXY_ENABLED"):
            request = HttpGeosurfProxyMiddleware.update_request(request, spider)
        else:
            if self.logging_enabled:
                spider.logger.warning('PROXY DISABLED')
                self.logging_enabled = False
