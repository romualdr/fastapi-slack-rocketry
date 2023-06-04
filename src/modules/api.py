import signal
from typing import Any, Coroutine, Optional
from fastapi import FastAPI
from kink import inject
import settings as settings
import uvicorn

from dependencies import IAsynchronousModule


api = FastAPI()


@api.get("/health")
async def health():
    return {"status": "ok"}


@inject(alias=IAsynchronousModule)
class APIModule(IAsynchronousModule):
    config: uvicorn.Config
    server: "APIModule.Server"

    class Server(uvicorn.Server):
        """Customized uvicorn.Server

        Uvicorn server overrides signals and we need to include
        Rocketry to the signals."""

        def install_signal_handlers(self) -> None:
            # Don't install signals - those will be handled by the main application
            return

    def __init__(self) -> None:
        self.config = uvicorn.Config(
            api,
            host="0.0.0.0",
            port=settings.PORT,
            log_level="debug" if settings.ENV_MODE != "production" else None,
            loop="asyncio",
            reload=settings.ENV_MODE != "production",
        )
        self.server = self.Server(config=self.config)

    def start(self) -> Coroutine[Any, Any, None]:
        return self.server.serve()

    async def stop(self, _signal: Optional[int]) -> None:
        self.server.handle_exit(_signal or signal.SIGINT, None)
