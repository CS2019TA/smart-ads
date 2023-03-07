import asyncio
import psutil

from fogverse import Producer
from fogverse.logging import CsvLogging
from fogverse.util import get_timestamp_str


class CPUProducer(CsvLogging, Producer):
    def __init__(self, loop=None):
        self.producer_topic = 'cpu-utilization' # replace with your kafka server IP address
        self.producer_servers = '192.168.1.18:9092'
        self.index = 1
        self.auto_decode = False
        CsvLogging.__init__(self)
        Producer.__init__(self, loop=loop)

    async def receive(self):
        cpu = str(psutil.cpu_percent())
        return cpu

    async def send(self, data):
        key = str(self.index).encode()
        headers = [
            ('index', str(self.index).encode()),
            ('timestamp', get_timestamp_str().encode())]
        await super().send(data, key=key, headers=headers)
        self.index += 1


async def main():
    producer = CPUProducer()
    tasks = [producer.run()]

    try:
        await asyncio.gather(*tasks)
    except:
        for t in tasks:
            t.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()