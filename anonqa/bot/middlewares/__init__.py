from aiogram import Dispatcher

from ...shared.config import Config


def register(dp: Dispatcher, config: Config):
    from . import throttling

    throttling.register_middleware(dp=dp, config=config)
