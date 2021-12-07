from scrapy import Spider, Request, Spider, signals
from scrapy.http import Response
import logging
from datetime import datetime, timedelta

class ForwardMetaMiddleware:
    """This middleware allows spiders to forward meta from response to request"""

    def __init__(self):
        self.last_meta = None

    def process_request(self, request: Request, spider: Spider):
        if self.last_meta:
            request.meta += self.last_meta

    def process_response(self, request: Request, response: Response, spider: Spider):
        meta = getattr(response, "meta", None)
        if meta:
            self.last_meta = meta
        logging.info(meta)
        return response
