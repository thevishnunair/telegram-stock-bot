
import os
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
session_name = 'stock_session'
source_channel = 'https://t.me/TradewixTrust'
destination_channel = 'https://t.me/+Ery86ayi9LpiM2Y1'

client = TelegramClient(session_name, api_id, api_hash)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    if event.message.video or event.message.document and 'video' in event.message.document.mime_type:
        return

    if event.message.grouped_id and event.message.media:
        messages = await client.get_messages(source_channel, grouped_id=event.message.grouped_id)
        for msg in messages:
            if msg.video or (msg.document and 'video' in msg.document.mime_type):
                return

    if event.message.media and isinstance(event.message.media, MessageMediaPhoto):
        await client.send_file(destination_channel, event.message.media, caption=event.message.text or "")
    elif event.message.message:
        await client.send_message(destination_channel, event.message.message)

print("✅ Bot is running... waiting for messages.")
client.start()
client.run_until_disconnected()
