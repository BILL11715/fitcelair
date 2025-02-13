from confluent_kafka import Consumer as KafkaConsumer, Producer as KafkaProducer
from util.config import config


def commit_completed(err, partitions):
    if err:
        print(str(err))
    else:
        print("Committed partition offsets: " + str(partitions))


class Kafka(object):
    def getConsumer():
        config["consumer_broker"].update({"on_commit": commit_completed})
        return KafkaConsumer(config["consumer_broker"])

    def getProducer():
        return KafkaProducer(config["kafka_broker"])
