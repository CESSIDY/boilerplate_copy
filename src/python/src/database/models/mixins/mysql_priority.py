from sqlalchemy import text
from sqlalchemy.dialects.mysql import MEDIUMINT
from sqlalchemy.sql.schema import Column


class MysqlPriorityMixin:
    PRIORITY_INITAL = 0
    PRIORITY_LOW = 1
    PRIORITY_MEDIUM = 2
    PRIORITY_HIGH = 3
    PRIORITY_CRITICAL = 4

    priority = Column("priority", MEDIUMINT(unsigned=True),
                      index=True,
                      unique=False,
                      nullable=False,
                      server_default=text("0"))

