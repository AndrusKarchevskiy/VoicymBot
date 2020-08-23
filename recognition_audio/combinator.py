import ffmpeg
from pydub import AudioSegment


def combine_audio_segments(voice_file_path: str, mem_file_path: str, user_id: int, quantity_sent_audios: int):
    try:
        voice = AudioSegment.from_file(f"data/voices/bot_voices/{user_id}_{quantity_sent_audios}.wav")
    except FileNotFoundError:
        voice = AudioSegment.from_file(f"data/voices/users_voices/{user_id}_{quantity_sent_audios}.wav")
    mem = AudioSegment.from_file(mem_file_path)

    ready_mem = voice + mem
    ogg_path = f"data/voices/ready_mems/{user_id}_{quantity_sent_audios}_stereo.ogg"
    ready_mem.export(ogg_path, format="ogg")

    # Без этого эта хуйня (вк) не работает (без перевода в моно-режим)!!!
    ffmpeg.input(f"data/voices/ready_mems/{user_id}_{quantity_sent_audios}_stereo.ogg").output(
        f"data/voices/ready_mems/{user_id}_{quantity_sent_audios}_mono.ogg", ac=1).run()


def mem_file_path_former(mem_name: str) -> str:
    if mem_name == '🐺Цитаты Волка':
        file_path = f"data/voices/mem_base_tracks/wolf-quotes.wav"
    elif mem_name == '🥁Бадабумц':
        file_path = f"data/voices/mem_base_tracks/badumtss.wav"
    elif mem_name == '👏Falcon Punch':
        file_path = f"data/voices/mem_base_tracks/falcon-punch.wav"
    elif mem_name == '🏅Just do it':
        file_path = f"data/voices/mem_base_tracks/just-do-it.wav"
    elif mem_name == '🎂Oh shit':
        file_path = f"data/voices/mem_base_tracks/oh-shit.wav"
    elif mem_name == '😔Грусть':
        file_path = f"data/voices/mem_base_tracks/sad.wav"
    elif mem_name == '😱Просто ор':
        file_path = f"data/voices/mem_base_tracks/scream.wav"
    elif mem_name == '🦊Снуп Догг':
        file_path = f"data/voices/mem_base_tracks/snoop-dogg.wav"
    elif mem_name == '🤖Hasta la vista, Baby':
        file_path = f"data/voices/mem_base_tracks/hasta-la-vista-baby.wav"
    else:
        file_path = None

    return file_path
