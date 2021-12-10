from scrapy import Spider, Request


class TestSpider(Spider):
    name = "test_spider"
    start_urls = ["https://docs.djangoproject.com/en/3.0/"]
    index = 0

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            'middlewares.UserAgentMiddleware': 1,
        }
    }

    def parse(self, response, **kwargs):
        self.logger.info(response.request.headers['User-Agent'])
        if self.index < 10:
            self.index += 1
            yield Request(
                url=self.start_urls[0],
                callback=self.parse,
                errback=self.errback,
                dont_filter=True,
            )
        return None

    def errback(self, failure):
        self.logger.error(failure)
