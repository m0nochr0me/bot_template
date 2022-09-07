"""
BotApp
Module
"""

from .confmaker import config
from .core import logger, db, _

__version__ = '0.0.1'

__all__ = ('logger', 'db', 'config', '_')

