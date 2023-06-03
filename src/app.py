"""
This file combines the two applications.
"""

import asyncio
import logging

logging.basicConfig(level=logging.DEBUG)

import uvicorn

from scheduler.public import scheduler
from slack.public import slack_socket
from api.public import api


class Server(uvicorn.Server):
    """Customized uvicorn.Server

    Uvicorn server overrides signals and we need to include
    Rocketry to the signals."""

    def handle_exit(self, sig: int, frame) -> None:
        scheduler.session.shut_down()
        loop.stop()
        return super().handle_exit(sig, frame)


if __name__ == "__main__":
    "Run the API and the scheduler"
    config = uvicorn.Config(
        api, host="0.0.0.0", port=3000, log_level="debug", loop="asyncio", reload=True
    )
    server = Server(config=config)

    loop = asyncio.get_event_loop()
    loop.create_task(server.serve())
    loop.create_task(slack_socket.connect_async())
    loop.create_task(scheduler.serve())
    loop.run_forever()
