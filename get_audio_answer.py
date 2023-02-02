import os
from get_text_answer import get_text_answer
from speech_to_text import convert_speach_to_text
from text_to_speech import convert_text_to_speech
from store import store_message
from langdetect import detect

def get_audio_answer(chat_id, audio_path):
    result = convert_speach_to_text(audio_path)
    history = store_message(chat_id, f'[USER] {result["text"].strip()}')
    text = get_text_answer(history).strip().replace("[AI]", "")
    store_message(chat_id, f'[AI] {text}')
    lang = detect(text)
    print('[lang]', lang)
    if lang != 'en':
        # remove audio files after sending
        if os.path.exists(audio_path):
            os.remove(audio_path)
        raise ValueError('Not supported language', text)

    convert_text_to_speech(text, audio_path)

    # remove audio files after sending
    if os.path.exists(file_path):
        os.remove(file_path)

    return text
