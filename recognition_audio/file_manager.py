import os
from pydub import AudioSegment
import aiohttp
import aiofiles


async def download_audio(url: str, user_id: int, quantity_sent_this_type_of_files: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(f'data/voices/users_voices/{user_id}_{quantity_sent_this_type_of_files}.mp3',
                                        mode='wb')
                await f.write(await resp.read())
                await f.close()

    await convert_mp3_to_wav(user_id=user_id, quantity_sent_this_type_of_files=quantity_sent_this_type_of_files)


async def convert_mp3_to_wav(user_id: int, quantity_sent_this_type_of_files: int):
    async with aiofiles.open(f"data/voices/users_voices/{user_id}_{quantity_sent_this_type_of_files}.wav", mode='wb'):
        pass

    src = f"data/voices/users_voices/{user_id}_{quantity_sent_this_type_of_files}.mp3"
    dst = f"data/voices/users_voices/{user_id}_{quantity_sent_this_type_of_files}.wav"

    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)).replace('recognition_audio', ''),
                        src.replace('/', '\\'))
    delete_file(path)


def delete_file(path):
    os.remove(path)
