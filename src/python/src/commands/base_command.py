# -*- coding: utf-8 -*-
import logging
from logging import Logger
from typing import Union

from scrapy.commands import ScrapyCommand
from scrapy.settings import Settings
from scrapy.utils.ossignal import install_shutdown_handlers
from scrapy.utils.project import get_project_settings
from twisted.enterprise import adbapi
from twisted.enterprise.adbapi import ConnectionPool
from MySQLdb.cursors import DictCursor
from sqlalchemy.dialects import mysql
from twisted.internet import reactor

class BaseCommand(ScrapyCommand):
    def __init__(self):
        super().__init__()
        self.db_connection_pool: Union[ConnectionPool, None] = None
        self.settings: Union[Settings, None] = None
        self.logger: Union[Logger, None] = None
        self.stopped: bool = False
        self._decorate_run()

    def _init(self):
        self.settings = get_project_settings()
        self.init_db_connection_pool()

        if not getattr(self, "logger", None):
            self.logger = logging.getLogger(name=self.__class__.__name__)

        install_shutdown_handlers(self.signal_shutdown_handler, True)

    def init_db_connection_pool(self):
        self.db_connection_pool = adbapi.ConnectionPool(
            "MySQLdb",
            host=self.settings.get("DB_HOST"),
            port=self.settings.getint("DB_PORT"),
            user=self.settings.get("DB_USERNAME"),
            passwd=self.settings.get("DB_PASSWORD"),
            db=self.settings.get("DB_DATABASE"),
            charset="utf8mb4",
            use_unicode=True,
            cursorclass=DictCursor,
            cp_reconnect=True,
        )

    def _decorate_run(self):
        def decorator(function):
            def wrapper(*args, **kwargs):
                self._init()
                self.init()
                return function(*args, **kwargs)

            return wrapper

        self.run = decorator(self.run)

    def signal_shutdown_handler(self, signal, frame):
        self.logger.info("received signal, `stopped` field changed")
        self.stopped = True

    def set_logger(self, name: str = "COMMAND", level: str = "DEBUG"):
        self.logger = logging.getLogger(name=name)
        self.logger.setLevel(level)

    def init(self):
        raise NotImplementedError("init method not implement")

    @staticmethod
    def compile_and_stringify_statement(stmt):
        return str(stmt.compile(compile_kwargs={"literal_binds": True}, dialect=mysql.dialect()))
