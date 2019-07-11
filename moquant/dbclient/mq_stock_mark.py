' Declaration of table `mq_stock_mark` '
__author__ = 'Momojie'

from sqlalchemy import Column, Integer, String, DECIMAL, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MqStockMark(Base):
    __tablename__ = 'mq_stock_mark'

    ts_code = Column('ts_code', String(10), primary_key=True)
    fetch_data = Column('fetch_data', Boolean)

    def __repr__(self):
        return 'code: %s, fetch_data: %s' % (self.ts_code, self.fetch_data)
