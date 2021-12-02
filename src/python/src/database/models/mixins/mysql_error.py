from sqlalchemy import text
from sqlalchemy.dialects.mysql import TEXT, SMALLINT, MEDIUMINT
from sqlalchemy.sql.schema import Column


class MysqlErrorMixin:
    PRIORITY_INITAL = 0
    PRIORITY_LOW = 1
    PRIORITY_MEDIUM = 2
    PRIORITY_HIGH = 3
    PRIORITY_CRITICAL = 4

    attempts_counter = Column("attempts_counter", SMALLINT(unsigned=True),
                              index=True, nullable=False,
                              server_default=text("0"))
    exception = Column("exception", TEXT,
                       nullable=True, index=False)
    priority = Column("priority", MEDIUMINT(unsigned=True),
                      index=True,
                      unique=False,
                      nullable=False,
                      server_default=text("0"))

