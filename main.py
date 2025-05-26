from telethon import TelegramClient, events
import asyncio
import os
from telethon.tl.types import MessageMediaDocument, DocumentAttributeVideo

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

source_channel = "https://t.me/tradevixtrust1"
target_channel = "https://t.me/+Ery86ayi9LpiM2Y1"

client = TelegramClient("stock_session", api_id, api_hash)

def contains_link(text):
    text = text.lower()
    return any(link in text for link in ["http", "https", "t.me", ".com", ".in"])

def is_video(msg):
    if isinstance(msg.media, MessageMediaDocument):
        for attr in msg.document.attributes:
            if isinstance(attr, DocumentAttributeVideo):
                return True
    return False

# ✅ Allow albums even if they contain videos
@client.on(events.Album(chats=source_channel))
async def album_handler(event):
    print("🎞️ Album received.")
    first_msg = event.messages[0]

    if first_msg.forward:
        print("⛔ Skipped album: Forwarded content.")
        return

    caption = first_msg.message or first_msg.text or ""
    if contains_link(caption):
        print("⛔ Skipped album: Contains link.")
        return

    try:
        await client.send_file(
            target_channel,
            [msg.media for msg in event.messages],
            caption=caption.strip() or "📸"
        )
        print("✅ Album posted.")
    except Exception as e:
        print(f"❌ Error posting album: {e}")

# ❌ Block standalone video messages
@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    msg = event.message
    text = msg.message or msg.text or ""

    print("📩 New message received.")
    print(f"📦 Content: '{text}'")

    if contains_link(text):
        print("⛔ Skipped: Link found.")
        return

    if msg.forward:
        print("⛔ Skipped: Forwarded content.")
        return

    if is_video(msg):
        print("⛔ Skipped: Single video message.")
        return

    try:
        await asyncio.sleep(0.5)
        if msg.media:
            print("📸 Media message detected. Sending...")
            await client.send_file(
                target_channel,
                file=msg.media,
                caption=text.strip() or "📸"
            )
            print("✅ Media sent.")
        else:
            print("💬 Text message detected. Sending...")
            await client.send_message(
                target_channel,
                text.strip() or "📤 [No text content]"
            )
            print("✅ Text sent.")
    except Exception as e:
        print(f"❌ Error sending message: {e}")

print("✅ Bot is running... waiting for messages.")
client.start()
client.run_until_disconnected()
