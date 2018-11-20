import ccxt
from .callback import Callback
import asyncio
from datetime import datetime

class BitmexOrderbookLoader(Callback):

    bitmex_api  = None
    logger      = None
    sleep_time  = None
    buckets     = None
    bucket_size = None
    pair        = None

    def __init__(self, pair, logger=None, sleep_time=300000, buckets=0, bucket_size=1):
        super().__init__("BitmexOrderbookLoader", logger=logger)
        self.sleep_time  = int(sleep_time)/1000
        self.bitmex_api  = ccxt.bitmex()
        self.buckets     = buckets
        self.bucket_size = bucket_size
        self.pair        = pair

    async def run(self):
        while True:

            try:
                # data retrieving
                order_book = bitmex_api.fetch_order_book(self.pair, limit=self.buckets)

                total_book   = {
                    **formatOrderBook(order_book["bids"]),
                    **formatOrderBook(order_book["asks"])
                }

                timestamp = datetime.utcnow().isoformat()
                messages = []
                for k, v in total_book.items():
                    messages += [{ "timestamp": timestamp, "pair": PAIR, "price": k, "amount": v }]

                self.logger.info("got %s buckets, going for sleep for %s sec" % (len(messages), self.sleep_time))
                await self.sendCallback(messages)
            except Exception as e:
                self.logger.exception("got exception, going for %s sleep" % self.sleep_time)
                self.logger.exception(e)

            await asyncio.sleep(self.sleep_time)

    def _formatOrderBook(bitmex_order_book):
        if type(bitmex_order_book) != list:
            raise Exception("bitmex_order_book should be list!")

        formatted_order_book = {}

        for order in bitmex_order_book:
            bucket_key = float(order[0] - order[0] % self.bucket_size)
            bucket_amount = formatted_order_book.get(bucket_key, 0)
            bucket_amount += order[1]
            #print("%s -> %s" % ( bucket_key, bucket_amount ))
            formatted_order_book[bucket_key] = bucket_amount

        return formatted_order_book
