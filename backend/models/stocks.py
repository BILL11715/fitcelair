import datetime
from mongoengine import Document, FloatField, EnumField, DateTimeField
from enum import Enum

"""["MSFT", "FB", "GOOG", "TSLA", "AMZN", "^GSPC"]"""


class Symbol(Enum):
    MSFT = "MSFT"
    FB = "FB"
    GOOG = "GOOG"
    TSLA = "TSLA"
    AMZN = "AMZN"
    GSPC = "^GSPC"


"""
TIME timestamp,           
SYMBOL text,              
OPEN float,               
HIGH float,               
LOW float,                
CLOSE float,              
VOLUME float,     
"""


class Stocks(Document):
    time = DateTimeField(required=True)
    symbol = EnumField(Symbol, default=Symbol.FB)
    open = FloatField(required=True)
    high = FloatField(required=True)
    low = FloatField(required=True)
    close = FloatField(required=True)
    volume = FloatField(required=True)
    created_at = DateTimeField(required=True, default=datetime.datetime.now())
    # updated_at = DateTimeField(required=True)

    # set dynamic updated_at and created_at fields values before save each stock
    def save(self, *args, **kargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datatime.now()
        return super(Stocks, self).save(*args, **kargs)
