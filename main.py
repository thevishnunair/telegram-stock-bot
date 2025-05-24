from telethon import TelegramClient, events
import os

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

source_channel = "https://t.me/owltradingcalls"
target_channel = "https://t.me/+Ery86ayi9LpiM2Y1"

client = TelegramClient("stock_session", api_id, api_hash)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    message = event.message.message
    if message and not any(link in message.lower() for link in ["http", "https", "t.me"]):
        await client.send_message(target_channel, message)

client.start()
client.run_until_disconnected()
