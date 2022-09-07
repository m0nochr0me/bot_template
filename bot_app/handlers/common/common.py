"""
BotApp
Common Handlers
"""

from contextlib import suppress
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified
from bot_app.models import Person, PersonSettings
from bot_app.core import _
from bot_app.util.buttons import Buttons as btn
from .keyboards import start_keyboard


async def cmd_start(obj: types.Message | types.CallbackQuery, state: FSMContext, locale):
    with suppress(MessageNotModified):
        await state.finish()
        user_id = obj.from_user.id
        user = await Person.find_one(Person.tg_id == user_id)
        if not user:
            user_settings = PersonSettings(locale=locale)
            user = Person(tg_id=user_id,
                          display_name=obj.from_user.first_name,
                          tg_username=obj.from_user.username,
                          settings=user_settings)
            await user.create()
        if isinstance(obj, types.CallbackQuery):
            await obj.answer()
            obj = obj.message
        keyboard = start_keyboard(locale=locale)
        await obj.answer(_('bot.welcome', locale=locale),
                         reply_markup=keyboard)


async def cmd_help(obj: types.Message | types.CallbackQuery, locale):
    if isinstance(obj, types.CallbackQuery):
        await obj.answer()
        obj = obj.message
    await obj.answer(_('bot.help', locale=locale))


async def cmd_eula(obj: types.Message | types.CallbackQuery, locale):
    if isinstance(obj, types.CallbackQuery):
        await obj.answer()
        obj = obj.message
    await obj.answer(_('bot.eula', locale=locale))


async def cmd_gdpr(obj: types.Message | types.CallbackQuery, locale):
    if isinstance(obj, types.CallbackQuery):
        await obj.answer()
        obj = obj.message
    await obj.answer(_('bot.gdpr', locale=locale))


async def cmd_about(obj: types.Message | types.CallbackQuery, locale):
    if isinstance(obj, types.CallbackQuery):
        await obj.answer()
        obj = obj.message
    await obj.answer(_('bot.about', locale=locale))


async def unregistered_user(obj: types.Message | types.CallbackQuery, locale):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=_('bot.btn.start', locale=locale), callback_data='btn_start'))
    if isinstance(obj, types.CallbackQuery):
        await obj.answer()
        obj = obj.message
    await obj.reply(_('bot.not_registered', locale=locale),
                    reply_markup=keyboard)


async def cmd_cancel(obj: types.Message | types.CallbackQuery, state: FSMContext, locale):
    await state.finish()
    if isinstance(obj, types.CallbackQuery):
        await obj.answer()
        obj = obj.message
    await obj.answer(
        _('bot.cancel', locale=locale),
        reply_markup=types.ReplyKeyboardRemove())


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start', state='*')
    dp.register_callback_query_handler(cmd_start, text=btn.START.value, state='*')

    dp.register_message_handler(cmd_help, commands='help')
    dp.register_callback_query_handler(cmd_help, text=btn.HELP.value)

    dp.register_message_handler(cmd_eula, commands='eula')
    dp.register_callback_query_handler(cmd_eula, text=btn.EULA.value)

    dp.register_message_handler(cmd_gdpr, commands='gdpr')
    dp.register_callback_query_handler(cmd_gdpr, text=btn.GDPR.value)

    dp.register_message_handler(cmd_about, commands='about')
    dp.register_callback_query_handler(cmd_about, text=btn.ABOUT.value)

    dp.register_message_handler(cmd_cancel, commands='cancel', state='*')
    dp.register_callback_query_handler(cmd_cancel, text=btn.CANCEL.value, state='*')

    dp.register_message_handler(unregistered_user, is_registered=False)
    dp.register_callback_query_handler(unregistered_user, is_registered=False)

