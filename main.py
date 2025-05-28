
import os
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
session_name = os.getenv('SESSION_NAME', 'stock_session')
source_channel = os.getenv('SOURCE_CHANNEL')
destination_channel = os.getenv('DESTINATION_CHANNEL')

client = TelegramClient(session_name, api_id, api_hash)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    try:
        message = event.message

        # Skip if it's a video or a live stream
        if message.video or message.video_note or message.document and message.document.mime_type and "video" in message.document.mime_type:
            print("Skipped a video or live stream.")
            return

        # Skip if it's part of an album with a video
        if message.grouped_id:
            messages = await client.get_messages(source_channel, grouped_id=message.grouped_id)
            if any(m.video or m.video_note or (m.document and m.document.mime_type and "video" in m.document.mime_type) for m in messages):
                print("Skipped album with a video.")
                return
            for m in messages:
                if m.photo or (m.document and m.document.mime_type.startswith("image")):
                    await client.send_file(destination_channel, m.media, caption=m.text if m.text else None)
            return

        # Post individual image with caption or text-only messages
        if message.photo or (message.document and message.document.mime_type.startswith("image")):
            await client.send_file(destination_channel, message.media, caption=message.text if message.text else None)
        elif message.text:
            await client.send_message(destination_channel, message.text)
        else:
            print("Skipped unsupported media type.")

    except Exception as e:
        print("Error while handling message:", e)

async def main():
    await client.start()
    print("✅ Bot is running... waiting for messages.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
