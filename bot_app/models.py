"""
BotApp
Models
"""

from datetime import datetime, timedelta
from pydantic import BaseModel
from beanie import Document, Indexed
from enum import Enum
from bot_app.confmaker import config


class Gender(Enum):
    FEMALE = 1
    MALE = 2
    OTHER = 3
    ATTACK_HELICOPTER = 4


class PersonSettings(BaseModel):
    locale: str = 'en'


class Person(Document):
    tg_id: Indexed(int, unique=True)
    display_name: str
    tg_username: str = None
    display_age: int = None
    gender: Gender = None
    registered: bool = False
    enabled: bool = False
    last_active: datetime = None
    settings: PersonSettings

    class Settings:
        name = 'persons'
        if config['beanie']['use_cache']:
            use_cache = True
            cache_expiration_time = timedelta(seconds=config['beanie']['ttl'])
            cache_capacity = config['beanie']['capacity']


__beanie_models__ = [Person]
