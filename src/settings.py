import argparse
import os
from .log import LOGGER
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--wtcke_kafka_url",              type=str, default=None)
parser.add_argument("--wtcke_marketcap_global_topic", type=str, default="marketcap_global")
parser.add_argument("--wtcke_marketcap_global_type",  type=str, default="global")
parser.add_argument("--wtcke_coin_marketcap_topic",   type=str, default="coin_marketcap")
parser.add_argument("--wtcke_coin_marketcap_type",    type=str, default="coin_marketcap")
parser.add_argument("--wtcke_sleep_ms",               type=int, default=300000)
parser.add_argument("--wtcke_coin_max_rank",          type=int, default=30)

args = parser.parse_args()

SETTINGS = {}
for a, v in vars(args).items():
    SETTINGS[a] = v

# override with env values if needed
for k, v in SETTINGS.items():
    if k.upper() in os.environ:
        SETTINGS[k] = os.environ.get(k.upper())

LOGGER.warn("starting app with settings: %s" % SETTINGS )
