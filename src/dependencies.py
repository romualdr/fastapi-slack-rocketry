from typing import Any, Coroutine, Optional, Union
from rocketry import Session
from rocketry.core import Task
from slack_sdk import WebClient


class ApplicationException(Exception):
    ...


class IAsynchronousModule:
    def start(self) -> Coroutine[Any, Any, None]:
        raise NotImplementedError()

    async def stop(self, _signal: Optional[int]) -> None:
        raise NotImplementedError()


class ISchedulerModule:
    def _get_current_session(self) -> Session:
        raise NotImplementedError()

    def find_task(self, task: Union[Task, str]) -> Optional[Task]:
        for task in self._get_current_session().tasks:
            if task == task or task.name == task:
                return task
        return None

    def get_task(self, task: Union[Task, str]) -> Task:
        found = self.find_task(task=task)
        if found is not None:
            return found

        raise Exception(f"Unable to find task {str(task)}")


class IChatClient(WebClient):
    pass
