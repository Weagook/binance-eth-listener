import asyncio
import json

from binance import AsyncClient, BinanceSocketManager

async def kline_listener(client):
    bm = BinanceSocketManager(client)
    async with bm.kline_socket(symbol='ETHUSDT') as stream:
        while True:
            res = await stream.recv()
            print(res['k']['c'])

async def main():

    client = await AsyncClient.create()
    await kline_listener(client)


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())