def form_welcome_message(user_name: str) -> str:
    welcome_message = f'🤝Привет, {user_name}!🤝\n\n' \
                      f'Я помогу тебе транслировать текст в голос и наоборот; сделать из голоса или текста -- ' \
                      f'аудио-мем.\n\n' \
                      f'Чтобы работать с ботом, нажимай на соответствующие клавиши'
    return welcome_message


def tell_send_voice() -> str:
    telling_message = 'Отлично! Теперь пришли голосовуху, а я постараюсь распознать текст😉'
    return telling_message


def tell_send_text_to_make_audio() -> str:
    telling_message = 'Отлично! Теперь пришли текст, который будем озвучивать😉'
    return telling_message


def tell_send_text_to_make_mem() -> str:
    telling_message = 'Отлично! Теперь пришли текст, который озвучит робот; вставит в мем😉'
    return telling_message


def tell_send_voice_to_make_mem() -> str:
    telling_message = 'Отлично! Теперь пришли войс (аудио-сообщение), которое робот вставит в мем😉'
    return telling_message


def tell_to_choose_mem() -> str:
    telling_message = 'Отлично! Теперь выбери мем, к котому прицепим готовое аудио😉'
    return telling_message


def tell_arg_not_correct() -> str:
    telling_message = '❌Введены некорректные данные...'
    return telling_message


def tell_arg_correct() -> str:
    telling_message = '🕑Принял! Скоро пришлю результат, жди'
    return telling_message


def tell_error_in_downloading() -> str:
    telling_message = '❌Ошибка скачивания. Пожалуйста, повтори попытку'
    return telling_message


def tell_error_in_voicing() -> str:
    telling_message = '❌Ошибка преобразование текста в голос. Повтор попытку, проверив корректность сообщения'
    return telling_message


def tell_to_push_button() -> str:
    telling_message = 'Нажми на одну из кнопок!'
    return telling_message
