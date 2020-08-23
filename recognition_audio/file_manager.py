import os
import requests
from pydub import AudioSegment


def download_audio(url: str, user_id: int, quantity_sent_this_type_of_files: int):
    req = requests.get(url, stream=True)
    with open(f'data/voices/users_voices/{user_id}_{quantity_sent_this_type_of_files}.mp3', 'wb') as file:
        file.write(req.content)

    convert_mp3_to_wav(user_id=user_id, quantity_sent_this_type_of_files=quantity_sent_this_type_of_files)


def convert_mp3_to_wav(user_id: int, quantity_sent_this_type_of_files: int):
    with open(f"data/voices/users_voices/{user_id}_{quantity_sent_this_type_of_files}.wav", 'wb'): pass
    src = f"data/voices/users_voices/{user_id}_{quantity_sent_this_type_of_files}.mp3"
    dst = f"data/voices/users_voices/{user_id}_{quantity_sent_this_type_of_files}.wav"

    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)).replace('recognition_audio', ''),
                        src.replace('/', '\\'))
    delete_file(path)


def delete_file(path):
    os.remove(path)
