from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

from ..shared.config import Config

users_commands = {
    "start": "Main menu",
    "help": "Show available commands",
}

admin_commands = {**users_commands, "ping": "Check bot ping", "stats": "Show bot stats"}


async def setup(bot: Bot, config: Config):
    await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in admin_commands.items()
        ],
        scope=BotCommandScopeChat(chat_id=config.main.owner_id),
    )

    await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in users_commands.items()
        ],
        scope=BotCommandScopeDefault(),
    )


async def remove(bot: Bot, config: Config):
    await bot.delete_my_commands(scope=BotCommandScopeDefault())
    await bot.delete_my_commands(
        scope=BotCommandScopeChat(chat_id=config.main.owner_id)
    )
