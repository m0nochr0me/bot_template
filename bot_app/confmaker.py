"""
BotApp
Configuration loader
"""

from yaml import safe_load
from mergedeep import merge

with open('config.yaml', mode='r', encoding='utf-8') as f:
    shared_config = safe_load(f)

with open('config.secret.yaml', mode='r', encoding='utf-8') as f:
    secret_config = safe_load(f)

config = merge(shared_config, secret_config)

