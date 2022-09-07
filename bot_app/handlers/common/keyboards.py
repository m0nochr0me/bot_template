from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot_app.core import _
from bot_app.util.buttons import Buttons as btn


def start_keyboard(locale='en') -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=3)

    keyboard.add(InlineKeyboardButton(text=_('bot.btn.register', locale=locale), callback_data=btn.REGISTER.value),
                 InlineKeyboardButton(text=_('bot.btn.locale', locale=locale), callback_data=btn.LOCALE.value),
                 InlineKeyboardButton(text=_('bot.btn.eula', locale=locale), callback_data=btn.EULA.value),
                 InlineKeyboardButton(text=_('bot.btn.gdpr', locale=locale), callback_data=btn.GDPR.value),
                 InlineKeyboardButton(text=_('bot.btn.help', locale=locale), callback_data=btn.HELP.value),
                 InlineKeyboardButton(text=_('bot.btn.about', locale=locale), callback_data=btn.ABOUT.value))
    return keyboard
