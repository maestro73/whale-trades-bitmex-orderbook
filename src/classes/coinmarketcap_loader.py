import ccxt
from .callback import Callback
import asyncio
from datetime import datetime

class CoinMarketCapLoader(Callback):

    cmk_api        = None
    logger         = None
    sleep_time     = None
    coins_max_rank = None

    EXTRACT_KEYS = {
        int: [ "rank", "last_updated" ],
        float: [
            "price_usd", "price_btc", "24h_volume_usd", "market_cap_usd", "available_supply",
            "percent_change_1h", "percent_change_24h", "percent_change_7d"
        ],
        str: [ "symbol" ]
    }
    EXTRACT_KEYS_T = {}

    def __init__(self, logger=None, sleep_time=60000, coins_max_rank=30):
        super().__init__("CoinMarketCapLoader", logger=logger)
        self.sleep_time = int(sleep_time)/1000
        self.cmk_api = ccxt.coinmarketcap()
        self.coins_max_rank = int(coins_max_rank)

        self.EXTRACT_KEYS_T = {}
        for t, field_list in self.EXTRACT_KEYS.items():
            for f in field_list:
                self.EXTRACT_KEYS_T[f] = t

    async def run(self):
        while True:

            # data retrieving
            currency_cap    = self.cmk_api.fetch_currencies()
            global_cap      = self.cmk_api.fetch_global()

            # field extracting + convertion
            filtered_ccap = [{
                ck: eval(self.EXTRACT_KEYS_T[ck].__name__)(cv) for ck, cv in coin_cap["info"].items() if ck in self.EXTRACT_KEYS_T.keys()
            } for symbol, coin_cap in currency_cap.items() if int(coin_cap["info"]["rank"]) <= self.coins_max_rank ]

            for x in filtered_ccap:
                x["timestamp"] = datetime.utcfromtimestamp(int(x["last_updated"])).isoformat()
                x["type"] = "coin_marketcap"

            global_cap["timestamp"] = datetime.utcfromtimestamp(int(global_cap["last_updated"])).isoformat()
            global_cap["type"] = "global"

            #self.logger.info("got full tick = %s, going for sleep for %s sec" % (tick, self.sleep_time))
            #await self.sendCallback(tick)

            self.logger.info("got coinmarketcap = [list: %s], global_cap = %s, going for sleep for %s sec" % (len(filtered_ccap), global_cap, self.sleep_time))

            for ccap_info in filtered_ccap:
                await self.sendCallback(ccap_info)
            await self.sendCallback(global_cap)

            await asyncio.sleep(self.sleep_time)
