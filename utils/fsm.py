from vkwave.bots.fsm import State


class GetterVoice:
    voice_message = State('voice_message')


class GetterText:
    text_message = State('text_message')


class GetterMemText:
    mem_text_message = State('mem_text_message')
    mem_type = State('mem_type')


class GetterMemAudio:
    mem_audio = State('mem_audio')
    mem_type = State('mem_type')
