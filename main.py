from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = 23553689
api_hash = '8fd8cfa43b86a969bb25e7fe8682628a'

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("✅ COPY THIS BASE64 SESSION STRING:")
    print(client.session.save())
