from sqlalchemy import text
from sqlalchemy.dialects.mysql import SMALLINT
from sqlalchemy.sql.schema import Column


class MysqlAttemptsCounterMixin:
    attempts_counter = Column("attempts_counter", SMALLINT(unsigned=True),
                              index=True, nullable=False,
                              server_default=text("0"))

