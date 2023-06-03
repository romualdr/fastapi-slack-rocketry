import os
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
NUM_WORKERS = int(os.getenv("NUM_WORKERS") or "2")
ENV_MODE = os.getenv("ENV_MODE")
PORT = int(os.getenv("PORT") or "3000")
