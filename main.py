
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import MessageMediaPhoto

api_id = 23553689
api_hash = '8fd8cfa43b86a969bb25e7fe8682628a'

session_string = "1BVtsOJsBu49O_n4WIZ-IknmMyfIZO4PdF_k7smzx7-5SMTnDTpX824FQWR2TnKfLZHE0GsNnghh7AEmp8-DxBQuIOwwO8raEgA4Lk96VeVxGjJW6akeCf3FqIh8X3Mg-ULu32hI4PBf-R8aRKiIuiyiTafPVCBbNH4idArbeUJyoLHSMMJ_ucPxJos2z5hE2psYndLKShy2m7yyndSxumEHMiiJSBhZHDsDlQvWzWXz1k_wTDxvrjLlGiGw-BpKPtD3YiEAkVQY3BYgCtlTT4LVHVGW-jQ3KuM1L8PaeL1ExoQz8Zfbkjs_YqgAqKrnUyorFA6wpMIXb46oZnQh9jm-VeBntVWo="

source_channel = 'https://t.me/tradevixtrust1'
destination_channel = 'https://t.me/+Ery86ayi9LpiM2Y1'

client = TelegramClient(StringSession(session_string), api_id, api_hash)

def message_has_link(message):
    if message.entities:
        for entity in message.entities:
            if hasattr(entity, 'url') or 'http' in message.message or 'www.' in message.message:
                return True
    return False

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    message = event.message

    if message_has_link(message):
        return

    if message.text and not message.media:
        await client.send_message(destination_channel, message.text)
        return

    if isinstance(message.media, MessageMediaPhoto):
        file = await message.download_media()
        await client.send_file(destination_channel, file, caption=message.text if message.text else None)
        return

    if hasattr(event, 'grouped_id') and event.grouped_id:
        messages = [m async for m in client.iter_messages(source_channel, min_id=message.id - 10, max_id=message.id + 10)
                    if m.grouped_id == message.grouped_id]
        media_files = []
        for m in messages:
            if isinstance(m.media, MessageMediaPhoto):
                media_files.append(await m.download_media())
            else:
                return
        await client.send_file(destination_channel, media_files)
        return

print("✅ Bot is running... waiting for messages.")
client.start()
client.run_until_disconnected()
