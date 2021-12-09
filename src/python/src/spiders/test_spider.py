from scrapy import Spider, Request


class TestSpider(Spider):
    name = "test_spider"
    start_urls = ["https://docs.djangoproject.com/en/3.0/"]
    index = 0

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            'middlewares.ForwardMetaMiddleware': 1,
        }
    }

    #meta_service_fields = ['download_timeout', 'download_slot', 'download_latency']

    def parse(self, response, **kwargs):
        if self.index < 10:
            self.index += 1
            yield Request(
                url=self.start_urls[0],
                callback=self.parse,
                meta={'test': 'test', f"key_{self.index}": f"result_{self.index}"},
                errback=self.errback,
                dont_filter=True,
            )
        return None

    def errback(self, failure):
        self.logger.error(failure)
