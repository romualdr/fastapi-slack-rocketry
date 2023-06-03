import asyncio
from rocketry import Rocketry
from slack.client import client

scheduler = Rocketry(execution="async")


@scheduler.task()
async def do_things(channel):
    await asyncio.sleep(10)
    client.chat_postMessage(channel=channel, text="Called inside scheduler !")
    ...
