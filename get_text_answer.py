import openai
import os

openai.api_key = os.environ.get('OPEN_AI_TOKEN')

def get_text_answer(text):
    print('[CHAT_GPT] Answering AI...')
    model_engine = "text-davinci-003"

    completion = openai.Completion.create(
        engine=model_engine,
        prompt=text,
        max_tokens=1024,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    print('[CHAT_GPT] Answer received!')

    return completion.choices[0].text