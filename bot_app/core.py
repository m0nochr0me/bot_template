"""
BotApp
Core Components
"""

import logging
import i18n
import asyncio
import motor.motor_asyncio
from pathlib import Path
from .confmaker import config


BASE_DIR = Path(__file__).parent

# Logger
logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
                    datefmt='%x %X',
                    filename=config['log']['logfile'],
                    level=logging.DEBUG,
                    encoding='utf-8')
logger = logging.getLogger('BotApp')


# DB
db_client = motor.motor_asyncio.AsyncIOMotorClient(config['mongo']['uri'])
db = db_client[config['mongo']['db']]


# i18n
i18n.load_path.append(BASE_DIR / 'locale')
i18n.set('fallback', 'en')
i18n.set('enable_memoization', True)
i18n.set('filename_format', '{locale}.yaml')
_ = i18n.t
locales = {
    'en': 'English',
    'pl': 'Polski',
    'uk': 'Українська',
    'ro': 'Română',
    'cz': 'Čeština',
    'ru': 'Русский',
}

