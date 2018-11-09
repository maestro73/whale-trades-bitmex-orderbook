from .settings      import SETTINGS
from .log           import LOGGER
from .classes       import CoinMarketCapLoader, KafkaCallback, PrintCallback
import asyncio
import functools

if not SETTINGS["wtcke_kafka_url"]:
    raise Exception("Kafka Url is not defined! App will exit...")

topic_mapping = {
    SETTINGS["wtcke_marketcap_global_type"] : SETTINGS["wtcke_marketcap_global_topic"],
    SETTINGS["wtcke_coin_marketcap_type"]   : SETTINGS["wtcke_coin_marketcap_topic"],
}

loader = CoinMarketCapLoader(logger=LOGGER, sleep_time=SETTINGS["wtcke_sleep_ms"], coins_max_rank=SETTINGS["wtcke_coin_max_rank"])
#p = PrintCallback()
kafka = KafkaCallback(SETTINGS["wtcke_kafka_url"],
    type_topic_mapping=topic_mapping,
    logger=LOGGER
)

loader.addCallback(kafka)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(loader.run())
