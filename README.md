
# FastAPI + Slack + Rocketry (async)

A Slack bot experiment, using FastAPI + Slack Bolt + Rocketry, running async with uvicorn

## Getting started

You'll need:
- Python 3
- ngrok
- A Slack bot

### Run it step by step
- Run ngrok
`./ngrok http 3000`

- Create a Slack bot from this manifest
```
display_information:
  name: MySuperTest
features:
  bot_user:
    display_name: MySuperTest
    always_online: true
  slash_commands:
    - command: /foo
      description: hey
      usage_hint: ya
      should_escape: false
oauth_config:
  redirect_urls:
    - https://fd29-146-70-194-55.ngrok-free.app # Replace with your ngrok URL
  scopes:
    bot: # Change scopes according to your needs
      - app_mentions:read
      - chat:write
      - files:write
      - commands
      - files:read
      - reactions:read
      - reactions:write
      - incoming-webhook
      - users:read
      - users.profile:read
      - channels:history
settings:
  event_subscriptions:
    bot_events:
      - app_mention
      - message.channels
  interactivity:
    is_enabled: true
  org_deploy_enabled: false
  socket_mode_enabled: true
  token_rotation_enabled: false
```

- Create `.env` with `cp .env.example .env`
- Go to your Slack app `OAuth & Permissions` and `Install the app` into your workspace
- Copy the `Bot User OAuth Token` value into `.env` at `SLACK_BOT_TOKEN`
- Go to your Slack app `Basic Information`, scroll to `App-Level Tokens`
- Use `Generate Token and Scopes` to create an app token, add some scopes, click on `Done`
- Copy the newly created `Token` into `.env` at `SLACK_APP_TOKEN`

- Install and run the server
```
pip install -r requirements.txt
python3 ./src/app.py
```
- Go to your Slack, invite your bot somewhere, type `@MySuperBot` or `/foo`
- Enjoy

## TODO
- Better file organisation + DI to avoid coupling between slack / scheduler
