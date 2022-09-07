from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot_app.core import _, locales
from aiogram.utils.callback_data import CallbackData
from bot_app.util.buttons import Buttons as btn

locale_callback = CallbackData('select_locale', 'value')


def keyboard_locales() -> InlineKeyboardMarkup:
    buttons = []

    for i in locales:
        buttons.append(InlineKeyboardButton(text=locales[i],
                                            callback_data=locale_callback.new(value=i)))
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    keyboard.add(InlineKeyboardButton(text=_('bot.btn.cancel'), callback_data=btn.CANCEL.value))
    return keyboard
