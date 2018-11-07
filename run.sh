#!/bin/bash

export LOG_LEVEL=INFO
export WTCKE_KAFKA_URL="localhost:9092"
export WTCKE_SLEEP_MS=120000
export WTCKE_COIN_MAX_RANK=50
export WTCKE_MARKETCAP_GLOBAL_TOPIC="global_marketcap"
export WTCKE_COIN_MARKETCAP_TOPIC="coin_marketcap"
set -e
python3 -m src
