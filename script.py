import subprocess
import openai
import whisper
import os
import re

openai.api_key = "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"

def getTextAnswer(text):
     # задаем модель и промпт
    model_engine = "text-davinci-003"

    print("Text question--->", text)

    # генерируем ответ
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=text,
        max_tokens=1024,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    print("text answer --->", completion.choices)
    return completion.choices[0].text

def getAudioAnswer(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio=audio_path, fp16=False)
    print("whisper result --->", result)
    text = getTextAnswer(result["text"])

    if (result['language'] != 'en'):
        raise ValueError('Not supported language', text)

    if not os.path.exists('answers-voice'):
        os.mkdir('answers-voice')

    textForReading = re.sub(r"[^a-zA-Z0-9,.'?! ]+", "", text)

    bashCommand = f'/home/kizilov/.local/bin/tts --text "{textForReading}" --out_path /home/kizilov/tts/answers-{audio_path}'
    subprocess.run(bashCommand, shell=True)
    return text