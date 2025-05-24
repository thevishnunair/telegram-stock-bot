from telethon import TelegramClient, events
import os

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

source_channel = "Tradewix Trust"
target_channel = "https://t.me/+Ery86ayi9LpiM2Y1"

client = TelegramClient("stock_session", api_id, api_hash)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    msg = event.message
    text = msg.message or ""
    caption = msg.text if msg.text else ""

    print("📩 New message detected!")
    print(f"📦 Message content: '{text}'")

    # Combine text and caption for filtering
    combined_text = f"{text} {caption}".lower()

    # ❌ Filter 1: Skip if message contains links
    if any(link in combined_text for link in ["http", "https", "t.me", ".com", ".in"]):
        print("⛔ Skipped due to link in text or caption.")
        return

    # ❌ Filter 2: Skip if the message is forwarded
    if msg.forward:
        print("⛔ Skipped because it's a forwarded message.")
        return

    try:
        if msg.media:
            print("📸 Media message detected. Sending...")
            await client.send_file(
                target_channel,
                file=msg.media,
                caption=text
            )
            print("✅ Media sent successfully.")
        else:
            print("💬 Text message detected. Sending...")
            await client.send_message(target_channel, text.strip() or "📤 [No text content]")
            print("✅ Text sent successfully.")
    except Exception as e:
        print(f"❌ Error while sending: {e}")

print("✅ Bot is running... waiting for messages.")
client.start()
client.run_until_disconnected()
