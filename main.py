import asyncio
from binance import AsyncClient, BinanceSocketManager
from datetime import datetime

first_time = datetime.now()
first_result = 0


async def kline_listener(client):
    global first_time
    global first_result

    bm = BinanceSocketManager(client)
    async with bm.kline_socket(symbol='ETHUSDT') as stream:
        while True:
            res = await stream.recv()
            res = float(res['k']['c'])
            new_time = datetime.now()
            passed = new_time - first_time
            passed = passed.total_seconds() // 60
            if passed >= 60:
                first_time = datetime.now()
            if res > first_result + first_result * 0.01 or res < first_result - first_result * 0.01:
                print('-----')
                print('Changes:')
                first_result = res
                print(first_result)
                print('-----')
                first_time = datetime.now()

async def main():

    client = await AsyncClient.create()
    await kline_listener(client)


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())