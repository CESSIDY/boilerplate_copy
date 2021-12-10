from scrapy import Spider, Request, Spider, signals
import logging
from datetime import datetime, timedelta
import random
import json

log = logging.getLogger('scrapy.useragent')

class Mode:
    RANDOMIZE_ONCE, RANDOMIZE_EVERY_REQUESTS, IN_ORDER_EVERY_REQUESTS = range(1,4) # 1, 2 ,3

class UserAgentMiddleware:
    """This middleware allows spiders to use the user_agent from list"""

    def __init__(self, *args, **kwargs):
        self.last_user_agent = None
        self.user_agent = None
        self.user_agents = None

    @classmethod
    def from_crawler(cls, crawler):
        o = cls()
        o.user_agent_release_data_checing(crawler)
        o.user_agent = crawler.settings['USER_AGENT']
        o.user_agents = crawler.settings['USER_AGENT_LIST']
        o.mode = crawler.settings['USER_AGENT_MODE']
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    @staticmethod
    def user_agent_release_data_checing(crawler):
        user_agent_release_date = crawler.settings['USER_AGENT_RELEASE_DATE']
        if datetime(*[int(number) for number in user_agent_release_date.split('-')]) + timedelta(days=180) < datetime.now():
            log.warning('USER_AGENT is outdated')

    def spider_opened(self, spider: Spider):
        self.user_agents = getattr(spider, 'user_agents', self.user_agents)
        self.mode = getattr(spider, 'user_agent_mode', self.mode)

    def process_request(self, request: Request, spider: Spider):
        if self.user_agents:
            request.headers.setdefault(b'User-Agent', self.get_user_agent_from_list())
        elif self.user_agent:
            request.headers.setdefault(b'User-Agent', self.user_agent)

    def get_user_agent_from_list(self):
        if self.mode == Mode.RANDOMIZE_ONCE:
            if not self.last_user_agent:
                user_agent = random.choice(list(self.user_agents))
                self.last_user_agent = user_agent
            else:
                user_agent = self.last_user_agent
        elif self.mode == Mode.RANDOMIZE_EVERY_REQUESTS:
            user_agent = random.choice(list(self.user_agents))
        elif self.mode == Mode.IN_ORDER_EVERY_REQUESTS:
            user_agent = self.user_agents.pop(0)
            self.user_agents.append(user_agent)
        log.info(user_agent)
        return str(user_agent).strip()
