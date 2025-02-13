#
import ast
import time
from util.util import string_to_float, symbol_list
from util.config import config
from confluent_kafka import Consumer as KafkaConsumer

# from cassandra.cluster import Cluster, NoHostAvailable
from producer import get_intraday_data


# =============================================================================
# Step 1: run zookeeper_starter.sh to start zookeeper
# Step 2: run kafka_starter.sh to start Kafka
# Step 3: run cassandra_starter.sh to start Cassandra
# Step 4: run producer.py to start sending data through Kafka
# =============================================================================


class CassandraStorage(object):

    """
    Kafka consumer reads the message and store the received data in Cassandra database

    """

    def __init__(self, symbol):
        if symbol == "^GSPC":
            self.symbol = "GSPC"
        else:
            self.symbol = symbol

        self.key_space = config["key_space"]

        # init a Cassandra cluster instance
        cluster = Cluster()

        # start Cassandra server before connecting
        try:
            self.session = cluster.connect()
        except NoHostAvailable:
            print("Fatal Error: need to connect Cassandra server")
        else:
            self.create_table()

    def create_table(self):
        """
        create Cassandra table of stock if not exist
        :return: None

        """
        self.session.execute(
            "CREATE KEYSPACE IF NOT EXISTS %s WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '3'} AND durable_writes = 'true'"
            % config["key_space"]
        )
        self.session.set_keyspace(self.key_space)

        # create table for intraday data
        self.session.execute(
            "CREATE TABLE IF NOT EXISTS {} ( \
                                    	TIME timestamp,           \
                                    	SYMBOL text,              \
                                    	OPEN float,               \
                                    	HIGH float,               \
                                    	LOW float,                \
                                    	CLOSE float,              \
                                        VOLUME float,             \
                                    PRIMARY KEY (SYMBOL,TIME));".format(
                self.symbol
            )
        )

    def kafka_consumer(self):
        """
        initialize a Kafka consumer
        :return: None

        """
        self.consumer1 = KafkaConsumer(config["topic_name1"], config["kafka_broker"])

    def stream_to_cassandra(self):
        """
        store streaming data of 1min frequency to Cassandra database
            :primary key: time,symbol
        :return: None

        """

        for msg in self.consumer1:
            # decode msg value from byte to utf-8
            dict_data = ast.literal_eval(msg.value.decode("utf-8"))

            # transform price data from string to float
            for key in ["open", "high", "low", "close", "volume"]:
                dict_data[key] = string_to_float(dict_data[key])

            query = "INSERT INTO {}(time, symbol,open,high,low,close,volume) VALUES ('{}','{}',{},{},{},{},{});".format(
                self.symbol,
                dict_data["time"],
                dict_data["symbol"],
                dict_data["open"],
                dict_data["high"],
                dict_data["low"],
                dict_data["close"],
                dict_data["volume"],
            )

            self.session.execute(query)
            print(
                "Stored {}'s min data at {}".format(
                    dict_data["symbol"], dict_data["time"]
                )
            )

    def delete_table(self, table_name):
        self.session.execute("DROP TABLE {}".format(table_name))


def main_realtime(symbol="^GSPC", tick=True):
    """
    main funtion to store realtime data; recommend to set tick=False, as getting tick data would cause rate limiting error from API
    """
    database = CassandraStorage(symbol)
    # database.kafka_consumer()kakf
    # database.stream_to_cassandra()kakf


def main_aftertradingday():
    """
    main function to update recent trading day's daily price (mainly for updating the adjusted close price), and 1min frequency price(to fill in empty data points caused by errors)
    """
    for symbol in symbol_list[:]:
        value_min, _ = get_intraday_data(symbol=symbol, outputsize="full", freq="1min")

        database = CassandraStorage(symbol)
        database.kafka_consumer()

        database.stream_to_cassandra(value_min, True)
        time.sleep(15)


if __name__ == "__main__":
    # update daily and 1 min freq data of all stocks
    # main_aftertradingday()
    # main_realtime(symbol='^GSPC',tick=True)
    # main_realtime_news()

    pass
