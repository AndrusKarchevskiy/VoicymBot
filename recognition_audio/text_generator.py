import speech_recognition as speech_rec

recog = speech_rec.Recognizer()


def get_text_from_voice(user_id, quantity_sent_audio_files):
    user_voice = speech_rec.AudioFile(f'data/voices/users_voices/{user_id}_{quantity_sent_audio_files}.wav')
    with user_voice as audio_file:
        audio_content = recog.record(audio_file)
        ready_text = '✔Вот, что мне удалось распознать:\n' \
                     '👉'
        try:
            ready_text += f'{recog.recognize_google(audio_content, language="ru-RU")}'
        except speech_rec.UnknownValueError:
            ready_text = 'К сожалению, мне ничего не удалось распознать... Повтори попытку'
    return ready_text
