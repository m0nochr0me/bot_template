"""
BotApp
Custom Middleware
"""

import i18n
from typing import Tuple, Optional, Any
from contextvars import ContextVar
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram import types
from babel import Locale
from bot_app.models import Person, PersonSettings


class GetLocaleMiddleware(LifetimeControllerMiddleware):

    ctx_locale = ContextVar('ctx_user_locale', default=None)
    skip_patterns = ['error', 'update']

    def __init__(self, fallback='en'):
        super().__init__()
        self.fallback = fallback

    async def get_user_locale(self) -> Optional[str]:
        user: Optional[types.User] = types.User.get_current()
        locale: Optional[Locale] = user.locale if user else None
        person: Optional[Person] = await Person.find_one(Person.tg_id == user.id) if user else None
        person_settings: Optional[PersonSettings] = person.settings if person else None

        if person_settings:
            language = person_settings.locale
        elif locale:
            language = locale.language
        else:
            language = self.fallback
        return language

    async def pre_process(self, obj, data, *args):
        locale = await self.get_user_locale()
        data['locale'] = locale
        self.ctx_locale.set(locale)

    async def post_process(self, obj, data, *args):
        del data['locale']
