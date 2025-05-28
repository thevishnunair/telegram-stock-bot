
import os
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
source_channel = "tradevixtrust1"
destination_channel = "https://t.me/+Ery86ayi9LpiM2Y1"

client = TelegramClient("session", api_id, api_hash)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    try:
        if event.message.video or event.message.video_note:
            print("Skipped: Video detected")
            return

        if event.message.grouped_id:
            messages = await client.get_messages(source_channel, limit=10)
            album = [m for m in messages if m.grouped_id == event.message.grouped_id]

            if any(m.video or m.video_note for m in album):
                print("Skipped: Album with video detected")
                return

            await client.send_file(destination_channel, [m.media for m in album if m.media], caption=album[0].text)
        elif event.message.media:
            await client.send_file(destination_channel, event.message.media, caption=event.message.text)
        else:
            await client.send_message(destination_channel, event.message.text)
    except Exception as e:
        print(f"Error: {e}")

print("✅ Bot is running... waiting for messages.")
client.start()
client.run_until_disconnected()
