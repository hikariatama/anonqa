import time

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from ...filters.is_admin import IsAdmin

router = Router()


@router.message(IsAdmin(is_admin=True), Command(commands=["ping"]))
async def ping_handler(message: Message):
    start = time.perf_counter_ns()
    reply_message = await message.answer("<code>⏱ Checking ping...</code>")
    end = time.perf_counter_ns()
    ping = (end - start) * 0.000001
    await reply_message.edit_text(f"<b>⏱ Ping -</b> <code>{ping:.3f}</code> <b>ms</b>")
