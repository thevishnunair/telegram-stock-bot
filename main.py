from telethon import TelegramClient, events
import os

# Environment variables
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# Use actual visible channel name
source_channel = "tatapunchgroup"
target_channel = "https://t.me/+Ery86ayi9LpiM2Y1"

client = TelegramClient("stock_session", api_id, api_hash)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    msg = event.message
    text = msg.message or ""

    print("📩 New message detected!")

    # Skip if there's a link
    if any(link in text.lower() for link in ["http", "https", "t.me"]):
        print("⛔ Skipped due to link in message.")
        return

    try:
        if msg.media:
            print("📸 Media message detected. Attempting to send...")
            await client.send_file(
                target_channel,
                file=msg.media,
                caption=text
            )
            print("✅ Media sent successfully.")
        elif text:
            print("💬 Text message detected.")
            await client.send_message(target_channel, text)
            print("✅ Text sent successfully.")
        else:
            print("⚠️ Message has no content or media.")
    except Exception as e:
        print(f"❌ Error while sending: {e}")

print("✅ Bot is running... waiting for messages.")
client.start()
client.run_until_disconnected()
