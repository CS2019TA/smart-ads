'''
ads.py and main.py are based on bellow source code
https://github.com/lemoncode21/fastapi-kafka
'''

from fastapi import FastAPI
import ads
import asyncio

app = FastAPI()

@app.get('/')
async def Home():
    return "welcome home"

app.include_router(ads.route)
asyncio.create_task(ads.consume())