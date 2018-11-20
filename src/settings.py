import argparse
import os
from log import LOGGER
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--wtbo_kafka_url",                        type=str, default=None)
parser.add_argument("--wtbo_marketcap_bitmex_orderbook_topic", type=str, default="bitmex_orderbook")
parser.add_argument("--wtbo_marketcap_bitmex_orderbook_type",  type=str, default="bitmex_orderbook")
parser.add_argument("--wtbo_pair",                             type=str, default="BTC/USD")
parser.add_argument("--wtbo_buckets",                          type=int, default=0)
parser.add_argument("--wtbo_bucket_size",                      type=int, default=5)
parser.add_argument("--wtbo_sleep_ms",                         type=int, default=300000)

args = parser.parse_args()

SETTINGS = {}
for a, v in vars(args).items():
    SETTINGS[a] = v

# override with env values if needed
for k, v in SETTINGS.items():
    if k.upper() in os.environ:
        SETTINGS[k] = os.environ.get(k.upper())

LOGGER.warn("starting app with settings: %s" % SETTINGS )
