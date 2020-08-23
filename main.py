import logging

from vkwave.api import Token, BotSyncSingleToken, API
from vkwave.bots import EventTypeFilter, SimpleLongPollBot, SimpleBotEvent, VoiceUploader
from vkwave.bots.fsm import FiniteStateMachine, StateFilter, ForWhat
from vkwave.client import AIOHTTPClient
from vkwave.types.bot_events import BotEventType

from data import config, template_messages as temp_msgs
from data.database import db
from recognition_audio import text_generator, voice_generator, file_manager, combinator
from utils.fsm import GetterText, GetterVoice, GetterMemText, GetterMemAudio
from utils.markups import DEFAULT_MARKUP, CANCEL_MARKUP, MEMS_MARKUP

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', )

client = AIOHTTPClient()
api = API(clients=client, tokens=BotSyncSingleToken(Token(config.BOT_TOKEN)), )

uploader = VoiceUploader(api.get_context())

bot = SimpleLongPollBot(tokens=config.BOT_TOKEN, group_id=config.GROUP_ID)

fsm = FiniteStateMachine()
bot.router.registrar.add_default_filter(StateFilter(fsm, ..., ..., always_false=True))
bot.router.registrar.add_default_filter(EventTypeFilter(BotEventType.MESSAGE_NEW.value))


async def get_user_data(message: bot.SimpleBotEvent) -> dict:
    user_data = (
        await bot.api_context.users.get(user_ids=message.object.object.message.peer_id)
    ).response[0]

    user_id = user_data.id
    user_full_name = f'{user_data.first_name} {user_data.last_name}'
    user_first_name = user_data.first_name
    text_from_message = message.object.object.message.text

    user_params = {'data': user_data,
                   'id': user_id,
                   'first_name': user_first_name,
                   'full_name': user_full_name,
                   'text_from_message': text_from_message}

    return user_params


@bot.message_handler(bot.text_filter(['начать', 'start', 'привет', 'hi']))
async def send_welcome(message: bot.SimpleBotEvent):
    user_data = await get_user_data(message)
    await db.add_new_user(user_id=user_data['id'], user_name=user_data['full_name'])
    await message.answer(temp_msgs.form_welcome_message(user_data['first_name']),
                         keyboard=DEFAULT_MARKUP)


@bot.message_handler(bot.text_filter('аудио ➡ текст'))
async def tell_to_send_voice(event: SimpleBotEvent):
    await fsm.set_state(event=event, state=GetterVoice.voice_message, for_what=ForWhat.FOR_USER)
    await event.answer(temp_msgs.tell_send_voice(), keyboard=CANCEL_MARKUP)


@bot.message_handler(StateFilter(fsm=fsm, state=GetterVoice.voice_message, for_what=ForWhat.FOR_USER), )
async def send_text_from_voice(event: SimpleBotEvent):
    user_data = await get_user_data(event)
    if user_data['text_from_message'] == 'Отмена':
        await event.answer('Отмена действия🔙', keyboard=DEFAULT_MARKUP)
        await fsm.finish(event=event, for_what=ForWhat.FOR_USER)

    else:
        try:
            if event.object.object.message.attachments[0].audio_message is not None:
                await event.answer(temp_msgs.tell_arg_correct(), keyboard=DEFAULT_MARKUP)
                url = event.object.object.message.attachments[0].audio_message.link_mp3

                try:
                    await db.update_user_param(user_id=user_data['id'], column='sent_audio_files')
                    quantity_sent_audio_files = await db.get_user_param(user_id=user_data['id'],
                                                                        column='sent_audio_files')

                    await file_manager.download_audio(url, user_data['id'], quantity_sent_audio_files)

                    await event.answer(text_generator.get_text_from_voice(user_data["id"], quantity_sent_audio_files))
                    file_manager.delete_file(path=f'data/voices/users_voices/{user_data["id"]}_'
                                                  f'{quantity_sent_audio_files}.wav')

                except:
                    await db.downgrade_user_param(user_id=user_data['id'], column='sent_audio_files')
                    await event.answer(temp_msgs.tell_error_in_downloading())

                await fsm.finish(event=event, for_what=ForWhat.FOR_USER)
            else:
                await event.answer(temp_msgs.tell_arg_not_correct())
        except IndexError:
            await event.answer(temp_msgs.tell_arg_not_correct())


@bot.message_handler(bot.text_filter('текст ➡ аудио'))
async def tell_to_send_text_to_make_audio(event: SimpleBotEvent):
    await fsm.set_state(event=event, state=GetterText.text_message, for_what=ForWhat.FOR_USER)
    await event.answer(temp_msgs.tell_send_text_to_make_audio(), keyboard=CANCEL_MARKUP)


@bot.message_handler(StateFilter(fsm=fsm, state=GetterText.text_message, for_what=ForWhat.FOR_USER), )
async def send_text_from_voice(event: SimpleBotEvent):
    user_data = await get_user_data(event)

    if user_data['text_from_message'] == 'Отмена':
        await event.answer('Отмена действия🔙', keyboard=DEFAULT_MARKUP)
        await fsm.finish(event=event, for_what=ForWhat.FOR_USER)

    else:
        # Если нет ошибки, то ивент содержит некорректный аргумент
        try:
            event.object.object.message.attachments[0]
            await event.answer(temp_msgs.tell_arg_not_correct())
        # Если заходим сюда -> сообщение от юзера корректно
        except IndexError:
            await event.answer(temp_msgs.tell_arg_correct(), keyboard=DEFAULT_MARKUP)

            await db.update_user_param(user_id=user_data['id'], column='sent_texts')
            quantity_sent_texts = await db.get_user_param(user_id=user_data['id'], column='sent_texts')

            try:
                voice_generator.text_to_base_woman_voice(user_data['id'], quantity_sent_texts,
                                                         user_data['text_from_message'])

                voice_file_path = f'data/voices/bot_voices/{user_data["id"]}_{quantity_sent_texts}.wav'

                bot_voice = await uploader.get_attachment_from_path(peer_id=user_data["id"], file_path=voice_file_path)
                await api.get_context().messages.send(user_id=user_data["id"], attachment=bot_voice, random_id=0)

                file_manager.delete_file(path=voice_file_path)

                await fsm.finish(event=event, for_what=ForWhat.FOR_USER)
            except:
                await event.answer(temp_msgs.tell_arg_not_correct())


@bot.message_handler(bot.text_filter('текст ➡ аудио-мем'))
async def tell_to_send_text_to_make_mem(event: SimpleBotEvent):
    await fsm.set_state(event=event, state=GetterMemText.mem_text_message, for_what=ForWhat.FOR_USER)
    await event.answer(temp_msgs.tell_send_text_to_make_mem(), keyboard=CANCEL_MARKUP)


@bot.message_handler(StateFilter(fsm=fsm, state=GetterMemText.mem_text_message, for_what=ForWhat.FOR_USER), )
async def send_mem_keyboard(event: SimpleBotEvent):
    user_data = await get_user_data(event)

    if user_data['text_from_message'] == 'Отмена':
        await event.answer('Отмена действия🔙', keyboard=DEFAULT_MARKUP)
        await fsm.finish(event=event, for_what=ForWhat.FOR_USER)

    else:
        # Если нет ошибки, то ивент содержит некорректный аргумент
        try:
            event.object.object.message.attachments[0]
            await event.answer(temp_msgs.tell_arg_not_correct())
        # Если заходим сюда -> сообщение от юзера корректно
        except IndexError:
            await db.update_user_param(user_id=user_data['id'], column='sent_texts')
            quantity_sent_texts = await db.get_user_param(user_id=user_data['id'], column='sent_texts')

            try:
                voice_generator.text_to_base_woman_voice(user_data['id'], quantity_sent_texts,
                                                         user_data['text_from_message'])
                await event.answer(temp_msgs.tell_to_choose_mem(), keyboard=MEMS_MARKUP)
                await fsm.finish(event=event, for_what=ForWhat.FOR_USER)
                await fsm.set_state(event=event, state=GetterMemText.mem_type, for_what=ForWhat.FOR_USER)
            except:
                await event.answer(temp_msgs.tell_arg_not_correct())


@bot.message_handler(StateFilter(fsm=fsm, state=GetterMemText.mem_type, for_what=ForWhat.FOR_USER), )
async def send_ready_mem(event: SimpleBotEvent):
    user_data = await get_user_data(event)
    # Если нет ошибки, то ивент содержит некорректный аргумент
    try:
        event.object.object.message.attachments[0]
        await event.answer(temp_msgs.tell_arg_not_correct())
    # Если заходим сюда -> сообщение от юзера корректно
    except IndexError:

        mem_file_path = combinator.mem_file_path_former(mem_name=user_data['text_from_message'])
        if mem_file_path is None:
            await event.answer(temp_msgs.tell_to_push_button())
        else:
            await fsm.finish(event=event, for_what=ForWhat.FOR_USER)
            quantity_sent_audios = await db.get_user_param(user_id=user_data['id'], column='sent_texts')
            voice_file_path = f"data/voices/bot_voices/{user_data['id']}_{quantity_sent_audios}.wav"
            combinator.combine_audio_segments(mem_file_path=mem_file_path,
                                              user_id=user_data['id'],
                                              quantity_sent_audios=quantity_sent_audios)
            await event.answer(temp_msgs.tell_arg_correct(), keyboard=DEFAULT_MARKUP)
            mem_path = f"data/voices/ready_mems/{user_data['id']}_{quantity_sent_audios}_mono.ogg"
            mem = await uploader.get_attachment_from_path(peer_id=user_data["id"], file_path=mem_path)
            await api.get_context().messages.send(user_id=user_data["id"], attachment=mem, random_id=0)

            file_manager.delete_file(path=voice_file_path)
            file_manager.delete_file(path=mem_path)
            file_manager.delete_file(path=mem_path.replace('mono', 'stereo'))


@bot.message_handler(bot.text_filter('аудио ➡ аудио-мем'))
async def tell_to_send_text_to_make_mem(event: SimpleBotEvent):
    await fsm.set_state(event=event, state=GetterMemAudio.mem_audio, for_what=ForWhat.FOR_USER)
    await event.answer(temp_msgs.tell_send_voice_to_make_mem(), keyboard=CANCEL_MARKUP)


@bot.message_handler(StateFilter(fsm=fsm, state=GetterMemAudio.mem_audio, for_what=ForWhat.FOR_USER), )
async def send_mem_keyboard(event: SimpleBotEvent):
    user_data = await get_user_data(event)

    if user_data['text_from_message'] == 'Отмена':
        await event.answer('Отмена действия🔙', keyboard=DEFAULT_MARKUP)
        await fsm.finish(event=event, for_what=ForWhat.FOR_USER)

    else:
        try:
            if event.object.object.message.attachments[0].audio_message is not None:
                url = event.object.object.message.attachments[0].audio_message.link_mp3
                try:
                    await db.update_user_param(user_id=user_data['id'], column='sent_audio_files')
                    quantity_sent_audio_files = await db.get_user_param(user_id=user_data['id'],
                                                                        column='sent_audio_files')

                    await file_manager.download_audio(url, user_data['id'], quantity_sent_audio_files)

                    await event.answer(temp_msgs.tell_to_choose_mem(), keyboard=MEMS_MARKUP)
                    await fsm.finish(event=event, for_what=ForWhat.FOR_USER)
                    await fsm.set_state(event=event, state=GetterMemAudio.mem_type, for_what=ForWhat.FOR_USER)
                except:
                    await db.downgrade_user_param(user_id=user_data['id'], column='sent_audio_files')
                    await event.answer(temp_msgs.tell_error_in_downloading())
            else:
                await event.answer(temp_msgs.tell_arg_not_correct())
        except IndexError:
            await event.answer(temp_msgs.tell_arg_not_correct())


@bot.message_handler(StateFilter(fsm=fsm, state=GetterMemAudio.mem_type, for_what=ForWhat.FOR_USER), )
async def send_ready_mem(event: SimpleBotEvent):
    user_data = await get_user_data(event)
    # Если нет ошибки, то ивент содержит некорректный аргумент
    try:
        event.object.object.message.attachments[0]
        await event.answer(temp_msgs.tell_arg_not_correct())
    # Если заходим сюда -> сообщение от юзера корректно
    except IndexError:
        mem_preset_path = combinator.mem_file_path_former(mem_name=user_data['text_from_message'])
        if mem_preset_path is None:
            await event.answer(temp_msgs.tell_to_push_button())
        else:
            await fsm.finish(event=event, for_what=ForWhat.FOR_USER)
            await event.answer(temp_msgs.tell_arg_correct(), keyboard=DEFAULT_MARKUP)
            quantity_sent_audios = await db.get_user_param(user_id=user_data['id'], column='sent_audio_files')
            voice_file_path = f"data/voices/users_voices/{user_data['id']}_{quantity_sent_audios}.wav"
            combinator.combine_audio_segments(
                mem_file_path=mem_preset_path, user_id=user_data['id'], quantity_sent_audios=quantity_sent_audios)

            mem_path = f"data/voices/ready_mems/{user_data['id']}_{quantity_sent_audios}_mono.ogg"

            mem = await uploader.get_attachment_from_path(peer_id=user_data["id"], file_path=mem_path)
            await api.get_context().messages.send(user_id=user_data["id"], attachment=mem, random_id=0)

            file_manager.delete_file(path=mem_path)
            file_manager.delete_file(path=mem_path.replace('mono', 'stereo'))
            file_manager.delete_file(path=voice_file_path)


@bot.message_handler()
async def send_markup_on_wrong_message(event: SimpleBotEvent):
    await event.answer(temp_msgs.tell_to_push_button(), keyboard=DEFAULT_MARKUP)


bot.run_forever()
