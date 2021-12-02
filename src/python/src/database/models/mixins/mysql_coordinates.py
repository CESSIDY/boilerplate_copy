from sqlalchemy import text
from sqlalchemy.dialects.mysql import DECIMAL
from sqlalchemy.sql.schema import Column


class MysqlCoordinatesMixin:
    latitude = Column("latitude", DECIMAL(8,6), nullable=True)
    longitude = Column("longitude", DECIMAL(9,6), nullable=True)
