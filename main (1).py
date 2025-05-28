
import os
import re
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_name = "stock_session"
source_channel = os.environ.get("SOURCE_CHANNEL")  # Exact username or ID (e.g., 'source_channel')
destination_channel = os.environ.get("DESTINATION_CHANNEL")  # Exact username or ID (e.g., 'destination_channel')

def contains_link(text):
    return bool(re.search(r'https?://|t\.me/|www\.', text or ''))

def is_allowed_album(messages):
    return all(
        isinstance(m.media, MessageMediaPhoto) and not contains_link(m.message)
        for m in messages if m.media
    )

client = TelegramClient(session_name, api_id, api_hash)

@client.on(events.Album())
async def handler_album(event):
    if event.chat.username != source_channel.lstrip("@"):
        return
    if is_allowed_album(event.messages):
        await client.send_album(destination_channel, event.messages)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    if event.grouped_id:
        return  # skip single message in an album; handled separately
    msg = event.message
    if contains_link(msg.message):
        return
    if msg.media:
        if isinstance(msg.media, MessageMediaPhoto):
            await client.send_file(destination_channel, file=msg.media, caption=msg.message or "")
        elif isinstance(msg.media, MessageMediaDocument):
            return  # skip videos, documents, etc.
    else:
        await client.send_message(destination_channel, msg.message)

print("✅ Bot is running... waiting for messages.")
client.start()
client.run_until_disconnected()
