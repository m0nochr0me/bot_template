"""
BotApp
CustomFilter
"""

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery
from .models import Person


class UserRegisteredFilter(BoundFilter):
    """
    Check if user is registered
    """

    key = 'is_registered'

    def __init__(self, is_registered: bool):
        self.is_registered = is_registered

    async def check(self, obj: Message | CallbackQuery) -> bool:
        return self.is_registered is await Person.find_one(Person.tg_id == obj.from_user.id).exists()

