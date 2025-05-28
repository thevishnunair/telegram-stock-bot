
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto

# Replace these with your own values
api_id = 23553689
api_hash = '8fd8cfa43b86a969bb25e7fe8682628a'
source_channel = 'https://t.me/tatapunchgroup'
destination_channel = 'https://t.me/+Ery86ayi9LpiM2Y1'

client = TelegramClient('anon', api_id, api_hash)

def message_has_link(message):
    if message.entities:
        for entity in message.entities:
            if hasattr(entity, 'url') or 'http' in message.message:
                return True
    return False

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    message = event.message

    # Filter out messages with links
    if message_has_link(message):
        return

    # Text-only message
    if message.text and not message.media:
        await client.send_message(destination_channel, message.text)
        return

    # Image-only message
    if isinstance(message.media, MessageMediaPhoto) and not message.text:
        await client.send_file(destination_channel, message.media.photo)
        return

    # Image with caption
    if isinstance(message.media, MessageMediaPhoto) and message.text:
        await client.send_file(destination_channel, message.media.photo, caption=message.text)
        return

    # Albums with only static images
    if hasattr(event, 'grouped_id') and event.grouped_id:
        messages = [m async for m in client.iter_messages(source_channel, min_id=message.id - 10, max_id=message.id + 10) if m.grouped_id == message.grouped_id]
        media_files = []
        for m in messages:
            if isinstance(m.media, MessageMediaPhoto):
                media_files.append(m.media.photo)
            else:
                return  # Skip album if any item is not a static image
        await client.send_file(destination_channel, media_files)
        return

print("✅ Bot is running... waiting for messages.")
client.start()
client.run_until_disconnected()
