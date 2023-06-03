import settings as settings
from scheduler.public import scheduler
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler


slack_app = AsyncApp(token=settings.SLACK_BOT_TOKEN)
slack_socket = AsyncSocketModeHandler(slack_app, settings.SLACK_APP_TOKEN)


@slack_app.command("/foo")
async def foo(ack, body, say):
    await ack()
    await say("bar")


@slack_app.event("app_mention")
async def handle_mentions(event, client, say):  # async function
    scheduler.session["do_things"].run({"channel": event["channel"]})
    await client.reactions_add(
        channel=event["channel"],
        timestamp=event["ts"],
        name="eyes",
    )
    await say("What's up?")
