from telethon import TelegramClient, events
import os

# Fetch environment variables
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# Define source and target channels
source_channel = "https://t.me/+I7XfJ2something"  # Replace with actual source invite link
target_channel = "https://t.me/+Ery86ayi9LpiM2Y1"

# Initialize the Telegram client
client = TelegramClient("stock_session", api_id, api_hash)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    msg = event.message
    text = msg.message or ""

    print("📩 New message detected!")

    # Skip messages with links
    if any(link in text.lower() for link in ["http", "https", "t.me"]):
        print("⛔ Skipped due to link in message.")
        return

    if msg.media:
        print("📸 Media message detected.")
        await client.send_file(
            target_channel,
            file=msg.media,
            caption=text
        )
    elif text:
        print("💬 Text message detected.")
        await client.send_message(target_channel, text)
    else:
        print("⚠️ Message has no content or media.")

print("✅ Bot is running... waiting for messages.")
client.start()
client.run_until_disconnected()
