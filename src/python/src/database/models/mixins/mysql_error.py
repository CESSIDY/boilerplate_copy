from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.sql.schema import Column


class MysqlErrorMixin:
    exception = Column("exception", TEXT,
                       nullable=True, index=False)

