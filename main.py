from telethon import TelegramClient, events
import os

# Fetch environment variables
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# Define source and target channels
source_channel = "https://t.me/+I7XfJ2something"  # Replace with your actual source channel invite link
target_channel = "https://t.me/+Ery86ayi9LpiM2Y1"  # Already known target channel

# Initialize the Telegram client
client = TelegramClient("stock_session", api_id, api_hash)

# Event handler for new messages
@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    msg = event.message
    text = msg.message or ""

    # Skip if text or caption has a link
    if any(link in text.lower() for link in ["http", "https", "t.me"]):
        return

    if msg.media:
        await client.send_file(
            target_channel,
            file=msg.media,
            caption=text
        )
    elif text:
        await client.send_message(target_channel, text)

# Start the client and run the bot
print("✅ Bot is running... waiting for messages.")
client.start()
client.run_until_disconnected()
