from sqlalchemy import text
from sqlalchemy.dialects.mysql import DECIMAL
from sqlalchemy.sql.schema import Column


class MysqlCoordinatesMixin:
    latitude = Column("latitude", DECIMAL(10, 8), nullable=True)
    longitude = Column("longitude", DECIMAL(11, 8), nullable=True)
