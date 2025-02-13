config = {
    "api_key": "D0UIG7NKI2XX6WCT",
    "symbol": "AAPL",
    "kafka_broker": {"bootstrap.servers": "localhost:9092"},
    "consumer_broker": {
        "bootstrap.servers": "localhost:9092",
        "group.id": "myid",
        "default.topic.config": {"auto.offset.reset": "earliest"},
    },
    # to transmit min data
    # "topic_name1": "stock_streaming",
    "topic_name1": "top1",
    "key_space": "stocks",
    "db": "streaming_db",
}


path = "C:/Users/ASUS/Desktop/Stock_streaming_project/"
path = "./"
timeZone = "US/Eastern"
