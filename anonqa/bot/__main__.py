import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram_dialog import DialogRegistry

from ..shared import config, db, log
from . import commands, handlers, middlewares


async def on_startup(
    dispatcher: Dispatcher,
    bot: Bot,
    config: config.Config,
    registry: DialogRegistry,
):
    middlewares.register(dp=dispatcher, config=config)

    dispatcher.include_router(handlers.get_router())

    await commands.setup(bot, config)
    await bot.delete_webhook(drop_pending_updates=False)

    bot_info = await bot.get_me()

    logging.info(f"Name - {bot_info.full_name}")
    logging.info(f"Username - @{bot_info.username}")
    logging.info(f"ID - {bot_info.id}")

    states = {
        True: "Enabled",
        False: "Disabled",
    }

    logging.debug(f"Groups Mode - {states[bot_info.can_join_groups]}")
    logging.debug(f"Privacy Mode - {states[not bot_info.can_read_all_group_messages]}")
    logging.debug(f"Inline Mode - {states[bot_info.supports_inline_queries]}")

    logging.error("Bot started!")


async def on_shutdown(dispatcher: Dispatcher, bot: Bot, config: config.Config):
    await bot.delete_webhook(drop_pending_updates=False)
    await dispatcher.fsm.storage.close()
    await bot.session.close()


async def main():
    logging.basicConfig(level=logging.INFO)
    cfg = config.parse(os.environ["CONFIG_PATH"])

    bot = Bot(cfg.main.token, parse_mode="HTML")

    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    registry = DialogRegistry(dp)

    await db.init()
    await dp.start_polling(bot, config=cfg, registry=registry)


if __name__ == "__main__":
    log.init()
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
