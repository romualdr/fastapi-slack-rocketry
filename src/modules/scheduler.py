import asyncio
from typing import Any, Coroutine, Optional
from kink import di, inject
from rocketry import Rocketry, Session


from dependencies import IAsynchronousModule, IChatClient, ISchedulerModule

scheduler = Rocketry(execution="async")


@scheduler.task()
async def do_things(channel):
    client: IChatClient = di[IChatClient]
    await asyncio.sleep(10)
    client.chat_postMessage(channel=channel, text="Called inside scheduler !")


@inject(alias=IAsynchronousModule)
@inject(alias=ISchedulerModule)
class SchedulerModule(IAsynchronousModule, ISchedulerModule):
    def _get_current_session(self) -> Session:
        return scheduler.session

    def start(self) -> Coroutine[Any, Any, None]:
        return scheduler.serve()

    async def stop(self, _signal: Optional[int]) -> None:
        scheduler.session.shut_down()
