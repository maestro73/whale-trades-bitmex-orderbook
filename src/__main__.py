import asyncio
import functools
import logging

# classes
from classes import *
# ##

# initializers
from settings import SETTINGS
from log      import LOGGER
# ##

try:

    if not SETTINGS["wtbo_kafka_url"]:
        raise Exception("Kafka Url is not defined! App will exit...")

    topic_mapping = {
        SETTINGS["wtbo_marketcap_bitmex_orderbook_type"] : SETTINGS["wtbo_marketcap_bitmex_orderbook_topic"],
    }

    loader = BitmexOrderbookLoader(SETTINGS["wtbo_pair"], sleep_time=SETTINGS["wtbo_sleep_ms"], buckets=SETTINGS["wtbo_buckets"], bucket_size=SETTINGS["wtbo_bucket_size"])

    kafka = KafkaCallback(SETTINGS["wtbo_kafka_url"], type_topic_mapping=topic_mapping)
    #print_c = PrintCallback()

    loader.addCallback(kafka)

    if __name__ == "__main__":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(loader.run())

except Exception as e:
    LOGGER.exception(e)
