from flask import Flask
from flask import request
from flask import Response
import requests
import os
from script import getAudioAnswer, getTextAnswer
 
TOKEN = "5787685011:AAFqdYOylKb4HFhfyvrjqa1l6yDNwEj6wGs"
app = Flask(__name__)
 
def parse_message(message):
    print("message-->",message)
    # if 'message' not in message: 
    #     raise ValueError('Cant find message')

    chat_id = message['message']['chat']['id']
    voice = message['message']['voice']['file_id'] if 'voice' in message['message'] else None
    txt = message['message']['text'] if 'text' in message['message'] else None

    return chat_id,txt,voice
 
def tel_send_message(chat_id, text):
    try:
        print("Sending text...")

        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': text
        }
    
        r = requests.post(url,json=payload)
        return r
    except ValueError as err:
        print('tel_send_message', err.args)

def tel_send_audio(chat_id, file_id):
    try:
        print("Sending audio...")

        get_file_url = f'https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}'
        file_response = requests.get(get_file_url).json()
        file_path = file_response["result"]["file_path"]
    
        audio_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
        audio_response = requests.get(audio_url)

        if not os.path.exists('voice'):
            os.mkdir('voice')

        with open(file_path, 'wb') as audio:
            audio.write(audio_response.content)
            text = getAudioAnswer(file_path)

            # remove audio files after sending
            if os.path.exists(file_path):
                os.remove(file_path)

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
                data=payload,
                files=files).json()

            # remove audio files after sending
            if os.path.exists(f'answers-{file_path}'):
                os.remove(f'answers-{file_path}')
    
        return resp
    except ValueError as err:
        print('tel_send_audio', err.args)
 
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        if 'message' not in msg: return Response('error', status=500)

        chat_id,txt,voice = parse_message(msg)

        if voice is not None:
            try:
                tel_send_audio(chat_id, voice)
            except ValueError as err:
                print(err.args)
                tel_send_message(chat_id, err.args[1])
            
        elif txt is not None:
            if txt.startswith('/'):
                tel_send_message(chat_id, 'Hi! Ask me something!')
            else:
                answer = getTextAnswer(txt)
                tel_send_message(chat_id, answer)

        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"
 
if __name__ == '__main__':
   app.run(debug=True)