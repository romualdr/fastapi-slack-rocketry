from slack_sdk import WebClient
import settings as settings

client = WebClient(token=settings.SLACK_BOT_TOKEN)
