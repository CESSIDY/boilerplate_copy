# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from w3lib.http import basic_auth_header
import random
import logging
from scrapy import Spider, Request, Spider
import uuid

log = logging.getLogger('scrapy.geosurf_proxy')

class HttpGeosurfProxyMiddleware:
    """
    This middleware allows spiders to use the geosurf proxy with random session code
    .env:
        TEMPLATE: GEOSURF_PROXY = <COUNTRY_CODE>-<SESSION_TIMEOUT>m.geosurf.io:8000
        EXAMPLE: GEOSURF_PROXY = "us-1m.geosurf.io:8000"

        TEMPLATE: GEOSURF_PROXY_AUTH = 601743+<COUNTRY_CODE_UPPERCASE>+601743-{session_code}:<YOURPASSWORD>
        EXAMPLE: GEOSURF_PROXY_AUTH = "601743+US+601743-{session_code}:43150a789"
    """

    logging_enabled = True
    proxy = None
    proxy_auth = None

    def __init__(self, settings):
        self.proxy_enabled: bool = bool(settings['PROXY_ENABLED']) if settings['PROXY_ENABLED'] else None
        if self.proxy_enabled:
            self._set_proxy_credential(settings)

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings)
        return o

    def _set_proxy_credential(self, settings: dict):
        proxy = settings.get('GEOSURF_PROXY', None)
        proxy_auth = settings.get('GEOSURF_PROXY_AUTH', None)

        if proxy and proxy_auth:
            self.proxy = proxy
            self.proxy_auth = proxy_auth
        else:
            log.error("Proxy enabled but not configured: GEOSURF_PROXY and GEOSURF_PROXY_AUTH need to be overridden")

    def update_request(self, request: Request, spider: Spider) -> Request:
        request.meta["proxy"] = self.modify_proxy(self.proxy)
        request.headers["Proxy-Authorization"] = self.modify_proxy_auth(self.proxy_auth)

        return request

    @staticmethod
    def modify_proxy(proxy):
        if "http" not in proxy:
            proxy = "http://{}".format(proxy)
        return proxy

    @staticmethod
    def modify_proxy_auth(proxy_auth):
        proxy_auth = proxy_auth.format(session_code=HttpGeosurfProxyMiddleware.get_random_session_code())
        return basic_auth_header(*proxy_auth.split(":"))

    @staticmethod
    def get_random_session_code():
        uid = str(uuid.uuid4())
        partial = "".join([f for f in uid if f.isdigit()])
        return partial[-6:]

    def process_request(self, request: Request, spider: Spider) -> None:
        if self._is_proxy_enabled:
            if self._is_proxy_configured():
                request = self.update_request(request, spider)
        else:
            if self.logging_enabled:
                spider.logger.warning('PROXY DISABLED')
                self.logging_enabled = False

    @staticmethod
    def _is_proxy_enabled(spider):
        return hasattr(spider, "proxy_enabled") and spider.proxy_enabled or spider.settings.get("PROXY_ENABLED")

    def _is_proxy_configured(self):
        return self.proxy and self.proxy_auth
