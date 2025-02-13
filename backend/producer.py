#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 12:57:07 2019

@author: yanyanyu

: get stock price every minute

"""

import json

import datetime

# import numpy as np
from pytz import timezone
from util.config import config
from util.util import symbol_list
from confluent_kafka import Producer

# from kafka import KafkaProducer
import requests

# =============================================================================
# Step 1: run zookeeper_starter.sh to start zookeeper
# Step 2: run kafka_starter.sh to start Kafka
# Step 3: run cassandra_starter.sh to start Cassandra
# Step 4: run producer.py to start sending data through Kafka
# =============================================================================

# logging.basicConfig(level=logging.DEBUG)


def get_intraday_data(symbol=symbol_list[0], outputsize="compact", freq="1min"):
    """
    :param outputsize: (str) 'compact' returns only the latest 100 data points in the intraday time series;
                             'full' returns the full-length intraday time series.
    :return: (dict) latest minute's stock price information
        e.g.:
            {"symbol": 'AAPL',
             "time"  : '2019-07-26 16:00:00',
             'open'  : 207.98,
             'high'  : 208.0,
             'low'   : 207.74,
             'close' : 207.75,
             'volume': 354454.0
            }
    """

    # get data using AlphaAvantage's API
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&outputsize={}&interval={}&apikey={}".format(
        symbol, outputsize, freq, config["api_key"]
    )
    print(url)
    req = requests.get(url)
    values = []

    # if request success
    if req.status_code == 200:
        raw_data = json.loads(req.content)
        try:
            price = raw_data["Time Series (1min)"]
            meta = raw_data["Meta Data"]
            # add each values data into list values
            for date in price:
                values.append(
                    {
                        "symbol": symbol,
                        "time": date,
                        "open": price[date]["1. open"],
                        "high": price[date]["2. high"],
                        "low": price[date]["3. low"],
                        "close": price[date]["4. close"],
                        "volume": price[date]["5. volume"],
                    }
                )

        except KeyError as e:
            print("error occured during format data", e)
            exit()

        time_zone = meta["6. Time Zone"]
        # price[freq] = price

        return values, time_zone
    else:
        print("  Failed: Cannot get {}'s data at {}:{} ".format(symbol, datetime))


def check_trading_hour(data_time):
    if data_time.time() < datetime.time(9, 30):
        last_day = data_time - datetime.timedelta(days=1)
        data_time = datetime.datetime(
            last_day.year, last_day.month, last_day.day, 16, 0, 0
        )

    elif data_time.time() > datetime.time(16, 0):
        data_time = datetime.datetime(
            data_time.year, data_time.month, data_time.day, 16, 0, 0
        )
    return data_time


def kafka_producer(producer, symbol="^GSPC"):

    # get data

    values, time_zone = get_intraday_data(symbol, outputsize="compact", freq="1min")

    now_timezone = datetime.datetime.now(timezone(time_zone))

    # try to set values into kafka server
    try:
        for date in values:
            producer.produce(
                config["topic_name1"],
                str(date),
            )
        producer.flush()

    except ValueError:
        print("error occured")
        exit()

    # display data length and time_zone
    print(len(values), now_timezone)


if __name__ == "__main__":
    # init an instance of KafkaProducer
    producer = Producer(config["kafka_broker"])

    # send data to kafka server
    kafka_producer(producer, symbol_list[4])

    pass
