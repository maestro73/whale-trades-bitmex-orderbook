#!/bin/bash

container_name="wtcke"

docker rmi $(docker images | grep ${container_name} | awk '{ print $1 }')
docker run --rm \
  --name=${container_name} \
  --network=host \
  -e "LOG_LEVEL=INFO" \
  -e "WTCKE_KAFKA_URL=localhost:9092" \
  -e "WTCKE_SLEEP_MS=120000" \
  -e "WTCKE_MARKETCAP_GLOBAL_TOPIC=global_marketcap" \
  -e "WTCKE_COIN_MARKETCAP_TOPIC=coin_marketcap" \
  -e "WTCKE_COIN_MAX_RANK=50" \
  dmi7ry/${container_name}:latest
