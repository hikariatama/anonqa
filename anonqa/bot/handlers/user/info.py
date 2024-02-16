from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from ....shared.config import Config
from ...commands import admin_commands, users_commands
from ...filters.is_admin import Dev

router = Router()


@router.message(Dev(), Command(commands=["help"]))
async def help_handler(message: Message, config: Config):
    text = "ℹ️ <b>Available commands:</b> \n\n"
    commands = (
        admin_commands.items()
        if message.from_user.id in config.main.admins
        else users_commands.items()
    )
    for command, description in commands:
        text += f"/{command} - <b>{description}</b> \n"
    await message.answer(text)
