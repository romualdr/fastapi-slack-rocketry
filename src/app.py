import asyncio
import signal
from logger import logger
from typing import List, Optional
from kink import inject
from dependencies import IAsynchronousModule

# Python don't see files / classes that are not imported
# As we're using dependency injection with kink, those files are never imported anywhere
# As a result, we need to import them to reference them into kink
# and be available for dependency injection (mostly here, in our main)
import modules.api  # noqa
import modules.messaging  # noqa
import modules.scheduler  # noqa


@inject()
class Application:
    modules: List[IAsynchronousModule]
    loop: asyncio.AbstractEventLoop
    signals: List[signal.Signals] = [
        signal.SIGINT,  # Unix signal 2. Sent by Ctrl+C.
        signal.SIGTERM,  # Unix signal 15. Sent by `kill <pid>`.
    ]

    def __init__(self, modules: List[IAsynchronousModule]) -> None:
        self.modules = modules
        self.loop = asyncio.get_event_loop()
        self.setup()

    def setup(self):
        for _signal in self.signals:
            self.loop.add_signal_handler(_signal, self.stop, _signal)

    def run(self):
        logger.info("Running application with event loop")
        for module in self.modules:
            self.loop.create_task(module.start())
        self.loop.run_forever()

    def stop(self, _signal: Optional[int]):
        logger.info("Stopping application ...")
        awaitables = []
        for module in self.modules:
            awaitables.append(module.stop(_signal=_signal))
        stop = asyncio.wait(awaitables)
        self.loop.create_task(stop)
        self.loop.stop()


if __name__ == "__main__":
    Application().run()
