from telethon import TelegramClient, events
import os

# Environment variables
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# Use actual visible channel name as seen in Telegram
source_channel = "tatapunchgroup"
target_channel = "https://t.me/+Ery86ayi9LpiM2Y1"

client = TelegramClient("stock_session", api_id, api_hash)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    msg = event.message
    text = msg.message or ""

    print("📩 New message detected!")

    if any(link in text.lower() for link in ["http", "https", "t.me"]):
        print("⛔ Skipped due to link in message.")
        return

    if msg.media:
        try:
            print("📸 Media message detected. Attempting to send...")
            await client.send_file(
                target_channel,
                file=msg.media,
                caption=text
            )
            print("✅ Media sent successfully.")
        except Exception as e:
            print(f"❌ Media failed: {e}")
    elif text:
        print("💬 Text message detected.")
        await client.send_message(target_channel, text)
    else:
        print("⚠️ Message has no content or media.")

print("✅ Bot is running... waiting for messages.")
client.start()
client.run_until_disconnected()
