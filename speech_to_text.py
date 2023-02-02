import whisper
def convert_speach_to_text(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio=audio_path, fp16=False)
    print('[STT]', result['text'])
    return result