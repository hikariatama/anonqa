import os

from aiogram import types
from aiogram.filters import Filter

from ...shared.config import Config, parse


class IsAdmin(Filter):
    def __init__(self, is_admin: bool) -> None:
        self.is_admin = is_admin

    async def __call__(self, message: types.Message, config: Config) -> bool:
        return self.is_admin is (message.from_user.id in config.main.admins)


class Dev(Filter):
    def __init__(self) -> None:
        self.is_dev = parse(os.environ["CONFIG_PATH"]).main.dev

    async def __call__(self, message: types.Message, config: Config) -> bool:
        return not self.is_dev or message.from_user.id in config.main.admins
