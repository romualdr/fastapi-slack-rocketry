import logging
import settings as settings

logging.basicConfig(
    level=logging.DEBUG if settings.ENV_MODE != "production" else logging.ERROR
)
logger = logging.getLogger("application")


def getLogger(name):
    return logging.getLogger(name)
