'''
ads.py and main.py are based on bellow source code
https://github.com/lemoncode21/fastapi-kafka
'''

import ads
import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def Home():
    return "welcome home"

app.include_router(ads.route)
asyncio.create_task(ads.consume())