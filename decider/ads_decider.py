import asyncio

from fogverse import Producer, Consumer, ConsumerStorage
from fogverse.logging import CsvLogging

class MyStorage(Consumer, ConsumerStorage):
    def __init__(self):
        Consumer.__init__(self)
        ConsumerStorage.__init__(self)