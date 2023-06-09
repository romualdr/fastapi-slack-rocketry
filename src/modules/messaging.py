from logger import getLogger
from typing import Any, Coroutine, Optional
from kink import di, inject
import settings as settings
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler

from dependencies import IAsynchronousModule, IChatClient, ISchedulerModule


slack_app = AsyncApp(token=settings.SLACK_BOT_TOKEN)
slack_socket = AsyncSocketModeHandler(slack_app, settings.SLACK_APP_TOKEN)


@slack_app.command("/foo")
async def foo(ack, body, say):
    await ack()
    await say("bar")


@slack_app.event("app_mention")
async def handle_mentions(event, client, say):  # async function
    scheduler: ISchedulerModule = di[ISchedulerModule]
    scheduler.get_task("do_things").run({"channel": event["channel"]})
    await client.reactions_add(
        channel=event["channel"],
        timestamp=event["ts"],
        name="eyes",
    )
    await say("What's up?")


@inject(alias=IChatClient)
class SlackClient(IChatClient):
    def __init__(self):
        super().__init__(
            token=settings.SLACK_BOT_TOKEN,
            logger=getLogger("SlackClient"),
        )


@inject(alias=IAsynchronousModule)
class MessagingModule(IAsynchronousModule):
    def start(self) -> Coroutine[Any, Any, None]:
        return slack_socket.connect_async()

    async def stop(self, _signal: Optional[int]) -> None:
        await slack_socket.close_async()
