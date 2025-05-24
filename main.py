from telethon import TelegramClient, events
import os

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

source_channel = "https://t.me/owltradingcalls"
target_channel = "https://t.me/+Ery86ayi9LpiM2Y1"

client = TelegramClient("stock_session", api_id, api_hash)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    message = event.message

    # Skip if message contains a link
    if message.message and any(link in message.message.lower() for link in ["http", "https", "t.me"]):
        return

    # If it's a media post (image, video, file, etc.)
    if message.media:
        await client.send_file(
            target_channel,
            file=message.media,
            caption=message.message or ""
        )
    else:
        # Plain text
        await client.send_message(target_channel, message.message)
