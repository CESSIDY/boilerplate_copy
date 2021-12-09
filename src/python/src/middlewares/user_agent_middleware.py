from scrapy import Spider, Request, Spider, signals
import logging
from datetime import datetime, timedelta

class UserAgentMiddleware:
    """This middleware allows spiders to use the user_agent from list"""

    def __init__(self) -> None:
        self.user_agents = None
        self.user_agent = None

    @classmethod
    def from_crawler(cls, crawler):
        o = cls()
        o.user_agent_release_data_checing(crawler)
        o.user_agent = crawler.settings['USER_AGENT']
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    @staticmethod
    def user_agent_release_data_checing(crawler):
        user_agent_release_date = crawler.settings['USER_AGENT_RELEASE_DATE']
        if datetime(*[int(number) for number in user_agent_release_date.split('-')]) + timedelta(days=180) < datetime.now():
            logging.warning('USER_AGENT is outdated')

    def spider_opened(self, spider: Spider):
        logging.info("Spider Open")
        self.user_agents = getattr(spider, 'user_agents', self.user_agents)

    def process_request(self, request: Request, spider: Spider):
        if self.user_agents:
            request.headers.setdefault(b'User-Agent', self.get_user_agent_from_list())
        elif self.user_agent:
            request.headers.setdefault(b'User-Agent', self.user_agent)

    def get_user_agent_from_list(self):
        user_agent = self.user_agents.pop(0)
        self.user_agents.append(user_agent)
        return str(user_agent).strip()
