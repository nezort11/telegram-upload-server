import io
import os
import base64
import json
import requests
import asyncio

from telethon import TelegramClient
from telethon.tl import types
from telethon.sessions import StringSession
from telethon.tl.types import DocumentAttributeAudio
from dotenv import load_dotenv
from flask import Flask, request, jsonify
# from requests_toolbelt.multipart import MultipartDecoder

load_dotenv()

APP_ID = os.getenv('APP_ID')
APP_HASH = os.getenv('APP_HASH')
PHONE = os.getenv('PHONE')
PASSWORD = os.getenv('PASSWORD')
SESSION = os.getenv('SESSION')
CHAT_ID = os.getenv('CHAT_ID')

app = Flask(__name__)

@app.route('/', methods=['POST'])
def send_audio():
    # print(request.headers)

    audio_stream = request.files['file']

    duration = int(request.form.get('duration') or 0)
    title = request.form.get('title')
    artist = request.form.get('artist')
    thumbnail = request.form.get('thumbnail')
    caption = request.form.get('caption')
    print('duration', duration)
    print('title', title)
    print('artist', artist)
    print('thumbnail', thumbnail)
    print('caption', caption)

    # data = request.get_json()

    # audio_url = data['file']
    # audio_bytes = base64.b64decode(data['file'])
    # audio_stream = io.BytesIO(audio_bytes)

    # duration = data['duration']
    # title = data['title']
    # artist = data['artist']
    # thumbnail = data['thumbnail']
    # caption = data['caption']

    # audio = requests.get(audio_url)
    # audio_stream = io.BytesIO(audio.content)
    audio_stream.name = 'audio.mp3' # required to tell telegram's ffmpeg it is MP3

    thumbnailBytes = None
    if thumbnail:
        thumbnailResponse = requests.get(thumbnail)
        thumbnailBytes = thumbnailResponse.content

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient(StringSession(SESSION), APP_ID, APP_HASH, loop=loop)
    client.start(PHONE, PASSWORD)

    message = client.loop.run_until_complete(client.send_file(CHAT_ID, audio_stream, caption=caption if caption else None, thumb=thumbnailBytes if thumbnailBytes else None, attributes=(DocumentAttributeAudio(duration, None, title if title else None, artist if artist else None),)))

    print('message_id', message.id)

    return jsonify({
        'chat_id': CHAT_ID,
        'message_id': message.id
    })

# def handler(event, context):
#     body = event['body']
#     # content_type = event['headers']['Content-Type']

#     # body_dec = base64.b64decode(body)
#     data = json.loads(body)

#     file_url = data['file']

#     # form_data = MultipartDecoder(body_dec, content_type)

#     # image_content = None
#     # for part in form_data.parts:
#     #     disposition = part.headers[b'Content-Disposition']
#     #     params = {}
#     #     for disposition_part in str(disposition).split(';'):
#     #         disposition_part_key_value = disposition_part.split('=', 2)
#     #         if len(disposition_part_key_value) > 1:
#     #             disposition_part_key = str(disposition_part_key_value[0]).strip()
#     #             disposition_part_value = str(disposition_part_key_value[1]).strip('\"\'\t \r\n')
#     #             params[disposition_part_key] = disposition_part_value

#     #     if params.get('name') == 'file':
#     #         image_content = part.content

#     # if image_content == None:
#     #     return {
#     #         'statusCode': 400
#     #     }

#     # image_stream = io.BytesIO(image_content)

#     file = requests.get(file_url)
#     file_stream = io.BytesIO(file.content)
#     file_stream.name = 'audio.mp3'

#     client = TelegramClient(StringSession(SESSION), APP_ID, APP_HASH)
#     client.start(PHONE, PASSWORD)

#     message = client.loop.run_until_complete(client.send_file(CHAT_ID, file_stream, attributes=(DocumentAttributeAudio(0),)))
#     #   attributes=[types.DocumentAttributeFilename('audio.mp3')], voice_note=True)
#     #   )
#     # message = client.loop.run_until_complete(client.send_file(CHAT_ID, file.content))
#     # message = client.loop.run_until_complete(client.send_file(CHAT_ID, file.content, voice_note=True))

#     return {
#         'statusCode': 200,
#         'headers': {
#             'Content-Type': 'application/json'
#         },
#         'isBase64Encoded': False,
#         'body': {
#             'chat_id': CHAT_ID,
#             'message_id': message.id
#         }
#     }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
