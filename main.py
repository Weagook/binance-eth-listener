import asyncio
from binance import AsyncClient, BinanceSocketManager
from datetime import datetime

# Create variables to store results and time
first_time = datetime.now()
first_result = 0


async def kline_listener(client):
    global first_time
    global first_result

    # We create a client
    bm = BinanceSocketManager(client)

    async with bm.kline_socket(symbol='ETHUSDT') as stream:
        while True:
            res = await stream.recv()
            # Choose only closed
            res = float(res['k']['c'])

            # Every time we check how much time has passed
            new_time = datetime.now()
            passed = new_time - first_time
            passed = passed.total_seconds() // 60

            # If 60 minutes have passed, reset the counter
            if passed >= 60:
                first_time = datetime.now()
                
            # If there were changes by 1 percent, we output information to the console and save the last result.
            if res > first_result + first_result * 0.01 or res < first_result - first_result * 0.01:
                print('-----')
                print('Changes:')
                first_result = res
                print(first_result)
                print('-----')
                first_time = datetime.now()

# Main function
async def main():
    client = await AsyncClient.create()
    await kline_listener(client)

# Trigger Condition
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())