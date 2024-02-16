import os

from aiogram import Bot

from ..shared import config

bot = Bot(token=config.parse(os.environ["CONFIG_PATH"]).main.token, parse_mode="HTML")
