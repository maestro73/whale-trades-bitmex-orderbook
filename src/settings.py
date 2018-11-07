import argparse
import os
from .log import LOGGER
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--wtcke_kafka_url",              help="url for kafka",                        type=str, default=None)
parser.add_argument("--wtcke_marketcap_global_topic", help="name of topic for global marketcap",   type=str, default="marketcap_global")
parser.add_argument("--wtcke_coin_marketcap_topic",   help="name of topic for price messages",     type=str, default="coin_marketcap")
parser.add_argument("--wtcke_sleep_ms",               help="sleep timeout between requests",       type=int, default=300000)
parser.add_argument("--wtcke_coin_max_rank",          help="total coins to fetch from market cap", type=int, default=30)

args = parser.parse_args()

SETTINGS = {}
for a, v in vars(args).items():
    SETTINGS[a] = v

# override with env values if needed
for k, v in SETTINGS.items():
    if k.upper() in os.environ:
        SETTINGS[k] = os.environ.get(k.upper())

LOGGER.warn("starting app with settings: %s" % SETTINGS )
