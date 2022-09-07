"""
BotApp
Locale Handler
"""

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot_app.models import Person, PersonSettings
from bot_app.core import _, locales
from bot_app.util.buttons import Buttons as btn
from .keyboards import keyboard_locales, locale_callback


class LocaleSelectStates(StatesGroup):
    wait_locale = State()


async def step_select_locale(obj: types.Message | types.CallbackQuery, locale):
    keyboard = keyboard_locales()
    if isinstance(obj, types.CallbackQuery):
        await obj.answer()
        obj = obj.message
    await obj.answer(_('bot.register.choose_locale', locale=locale),
                     reply_markup=keyboard)
    await LocaleSelectStates.wait_locale.set()


async def step_locale_confirm(call: types.CallbackQuery, state: FSMContext, callback_data: dict, locale):
    selected_locale = callback_data['value']
    person: Person = await Person.find_one(Person.tg_id == call.from_user.id)
    person_settings: PersonSettings = person.settings
    person_settings.locale = selected_locale
    person.settings = person_settings
    await person.save()
    await call.answer()
    await call.message.answer(_('bot.locale.selected', locale=selected_locale) + locales[selected_locale])
    await state.finish()


def register_handlers_locale(dp: Dispatcher):
    dp.register_message_handler(step_select_locale, commands=['lang', 'locale'], state='*')
    dp.register_callback_query_handler(step_select_locale, text=btn.LOCALE.value, state='*')

    # dp.register_message_handler(step_locale_confirm, state=LocaleSelectStates.wait_locale)
    dp.register_callback_query_handler(step_locale_confirm, locale_callback.filter(), state=LocaleSelectStates.wait_locale)
