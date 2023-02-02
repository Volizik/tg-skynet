import subprocess
import re
import os

def convert_text_to_speech(text, audio_path):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    DEST_DIR = os.path.join(ROOT_DIR, f'answers-{audio_path}')

    text_for_reading = re.sub(r"[^a-zA-Z0-9,.'?! ]+", "", text)

    bash_command = f'/home/kizilov/.local/bin/tts --text "{text_for_reading}" --out_path {DEST_DIR}'
    subprocess.run(bash_command, shell=True)