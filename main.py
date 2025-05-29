from telethon.sync import TelegramClient

# Replace with your actual values
api_id = 12345678
api_hash = 'your_api_hash_here'

with TelegramClient('render_session', api_id, api_hash) as client:
    session_string = client.session.save()
    print("\n✅ COPY THIS BASE64 SESSION STRING:\n")
    print(session_string)
