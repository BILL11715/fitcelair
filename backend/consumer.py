import ast
from confluent_kafka import Consumer as KafkaConsumer
from mongoengine import connect, disconnect
from models.kafka import Kafka
from models.stocks import Stocks
from services.kafkaMessages import get_kafka_messages
from util.util import string_to_float, symbol_list
from util.config import config


class MongoStorage(object):
    def __init__(
        self,
        symbol="GSPC",
    ) -> None:
        self.symbol = symbol

    def getMessagesFromKafka(self):
        data = get_kafka_messages()
        return data

    def stream_to_MongoDB(self):
        try:
            # connect to mongodb
            connect(config["db"])
        except ValueError:
            print("connection database failed")
            exit()
        try:
            messages = self.getMessagesFromKafka()
            if len(messages):
                storedIds = Stocks.objects.insert(messages, load_bulk=False)
                print({"storedIds": len(messages)})
                return True
            else:
                print("no data available messages:", messages)
        except NameError:
            print("Error occured during saving messages consumer to mongoDB")
        finally:
            # connect to mongodb
            disconnect(config["db"])


if __name__ == "__main__":
    # update daily and 1 min freq data of all stocks
    # main_aftertradingday()
    # main_realtime(symbol='^GSPC',tick=True)
    # main_realtime_news()
    mongostore = MongoStorage(symbol_list[0])
    mongostore.stream_to_MongoDB()
    print("ok")
    pass
