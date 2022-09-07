"""
BotApp
Registration Handler
"""

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot_app.models import PersonSettings, Person
from bot_app.core import _


class RegistrationStates(StatesGroup):
    wait_name = State()
    wait_age = State()


async def step_enter_name(message: types.Message, locale):
    await message.answer(_('bot.register.enter_name', locale=locale))
    await RegistrationStates.wait_name.set()


async def step_enter_age(message: types.Message, state: FSMContext, locale):
    user_input = message.text[:32]
    # name validation here
    await state.update_data(display_name=user_input)

    await RegistrationStates.next()
    await message.answer(_('bot.register.enter_age', locale=locale))


async def step_enter_age_is_invalid(message: types.Message, state: FSMContext, locale):
    return await message.answer(_('bot.register.age_digits_error', locale=locale))


async def step_enter_age_out_of_range(message: types.Message, state: FSMContext, locale):
    return await message.answer(_('bot.register.age_range_error', locale=locale))


async def step_registration_confirm(message: types.Message, state: FSMContext, locale):
    user_input = int(message.text)
    await state.update_data(display_age=user_input)

    person = await Person.find_one(Person.tg_id == message.from_user.id)

    data = await state.get_data()
    person.display_name = data['display_name']
    person.display_age = data['display_age']
    await person.save()

    await message.answer(_('bot.register.complete', locale=locale))
    await state.finish()


def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(step_enter_name, commands='register', state='*')
    dp.register_message_handler(step_enter_age, state=RegistrationStates.wait_name)
    dp.register_message_handler(step_enter_age_is_invalid,
                                lambda message: not message.text.isdigit(),
                                state=RegistrationStates.wait_age)
    dp.register_message_handler(step_enter_age_out_of_range,
                                lambda message: not 18 <= int(message.text) <= 99,
                                state=RegistrationStates.wait_age)
    dp.register_message_handler(step_registration_confirm, state=RegistrationStates.wait_age)

