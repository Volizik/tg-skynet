import requests
import os
from flask import Flask
from flask import request
from flask import Response
from dotenv import load_dotenv

from get_text_answer import get_text_answer
from get_audio_answer import get_audio_answer
from store import store_message, get_user_messages

load_dotenv()
 
TOKEN = os.environ.get('TG_TOKEN')
app = Flask(__name__)
 
def parse_message(message):
    print('[PARSE MESSAGE]', message)
    if 'message' in message:
        chat_id = message['message']['chat']['id']
        voice = message['message']['voice']['file_id'] if 'voice' in message['message'] else None
        txt = message['message']['text'] if 'text' in message['message'] else None

        return chat_id, txt, voice
    elif 'edited_message' in message:
        chat_id = message['edited_message']['chat']['id']
        voice = message['edited_message']['voice']['file_id'] if 'voice' in message['edited_message'] else None
        txt = message['edited_message']['text'] if 'text' in message['edited_message'] else None

        return chat_id, txt, voice
    else:
        raise ValueError('[PARSE MESSAGE] Unexpected error')
 
def tel_send_message(chat_id, text):
    try:
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': text
        }
    
        r = requests.post(url, json = payload)
        return r
    except ValueError as err:
        print('[Error][tel_send_message]', err.args)

def tel_send_audio(chat_id, file_id):
    get_file_url = f'https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}'
    file_response = requests.get(get_file_url).json()
    file_path = file_response["result"]["file_path"]

    audio_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
    user_audio_response = requests.get(audio_url)

    if not os.path.exists('voice'):
        os.mkdir('voice')

    with open(file_path, 'wb') as audio:
        audio.write(user_audio_response.content)
        text = get_audio_answer(chat_id, file_path)

    with open(f'answers-{file_path}', 'rb') as audio:
        payload = {
            'chat_id': chat_id,
            'title': 'file.mp3',
            'parse_mode': 'HTML',
        }
        files = {
            'audio': audio.read(),
        }
        resp = requests.post(
            f'https://api.telegram.org/bot{TOKEN}/sendAudio',
            data = payload,
            files = files).json()

        # remove audio files after sending
        if os.path.exists(f'answers-{file_path}'):
            os.remove(f'answers-{file_path}')

    return resp
 
@app.route('/', methods=['POST'])
def index():
    try:
        msg = request.get_json()
        chat_id, txt, voice = parse_message(msg)

        if voice is not None:
            try:
                tel_send_audio(chat_id, voice)
            except ValueError as err:
                print('[CATCH][Incoming request]', err.args)
                tel_send_message(chat_id, err.args[1])

        elif txt is not None:
            if txt.startswith('/'):
                tel_send_message(chat_id, 'Ask me anything!')
            else:
                history = store_message(chat_id, f'[USER] {txt}')
                answer = get_text_answer(history)
                store_message(chat_id, f'[AI] {answer.strip()}')
                tel_send_message(chat_id, answer.replace('[AI]', ''))
        print('[HISTORY] ', get_user_messages(chat_id))
        return Response('ok', status=200)
    except ValueError as err:
        return Response(f'[ERROR] {err}', status=500)
 
if __name__ == '__main__':
   app.run(debug=True)