from gtts import gTTS


def text_to_base_woman_voice(user_id: int, quantity_sent_texts: int, text: str):
    language = 'ru'
    file_path = f'data/voices/bot_voices/{user_id}_{quantity_sent_texts}.wav'
    speech = gTTS(text=text, lang=language, slow=False)
    speech.save(file_path)
