from vkwave.bots import Keyboard, ButtonColor

DEFAULT_MARKUP = Keyboard()
DEFAULT_MARKUP.add_text_button(text='Текст ➡ Аудио', color=ButtonColor.SECONDARY)
DEFAULT_MARKUP.add_row()
DEFAULT_MARKUP.add_text_button(text='Аудио ➡ Текст', color=ButtonColor.SECONDARY)
DEFAULT_MARKUP.add_row()
DEFAULT_MARKUP.add_text_button(text='Текст ➡ Аудио-мем', color=ButtonColor.SECONDARY)
DEFAULT_MARKUP.add_row()
DEFAULT_MARKUP.add_text_button(text='Аудио ➡ Аудио-мем', color=ButtonColor.SECONDARY)
DEFAULT_MARKUP = DEFAULT_MARKUP.get_keyboard()

CANCEL_MARKUP = Keyboard()
CANCEL_MARKUP.add_text_button(text='Отмена', color=ButtonColor.SECONDARY)
CANCEL_MARKUP = CANCEL_MARKUP.get_keyboard()

MEMS_MARKUP = Keyboard()
MEMS_MARKUP.add_text_button(text='🐺Цитаты Волка', color=ButtonColor.SECONDARY)
MEMS_MARKUP.add_text_button(text='🥁Бадабумц', color=ButtonColor.SECONDARY)
MEMS_MARKUP.add_row()
MEMS_MARKUP.add_text_button(text='👏Falcon Punch', color=ButtonColor.SECONDARY)
MEMS_MARKUP.add_text_button(text='🏅Just do it', color=ButtonColor.SECONDARY)
MEMS_MARKUP.add_row()
MEMS_MARKUP.add_text_button(text='🎂Oh shit', color=ButtonColor.SECONDARY)
MEMS_MARKUP.add_text_button(text='😔Грусть', color=ButtonColor.SECONDARY)
MEMS_MARKUP.add_row()
MEMS_MARKUP.add_text_button(text='😱Просто ор', color=ButtonColor.SECONDARY)
MEMS_MARKUP.add_text_button(text='🦊Снуп Догг', color=ButtonColor.SECONDARY)
MEMS_MARKUP.add_row()
MEMS_MARKUP.add_text_button(text='🤖Hasta la vista, Baby', color=ButtonColor.SECONDARY)
MEMS_MARKUP = MEMS_MARKUP.get_keyboard()
