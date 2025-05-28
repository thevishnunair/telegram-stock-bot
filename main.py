
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto

# Replace with your own values
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

grouped_messages = {}

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    message = event.message

    if message_has_link(message):
        return

    if message.grouped_id:
        gid = message.grouped_id
        if gid not in grouped_messages:
            grouped_messages[gid] = []
        grouped_messages[gid].append(message)
        await asyncio.sleep(2)
        if len(grouped_messages[gid]) > 1:
            media_files = []
            for msg in grouped_messages[gid]:
                if isinstance(msg.media, MessageMediaPhoto):
                    media_files.append(msg.media.photo)
                else:
                    return
            await client.send_file(destination_channel, media_files)
            del grouped_messages[gid]
        return

    if message.text and not message.media:
        await client.send_message(destination_channel, message.text)
    elif isinstance(message.media, MessageMediaPhoto) and not message.text:
        await client.send_file(destination_channel, message.media.photo)
    elif isinstance(message.media, MessageMediaPhoto) and message.text:
        await client.send_file(destination_channel, message.media.photo, caption=message.text)

print("✅ Bot is running... waiting for messages.")
client.start()
client.run_until_disconnected()
