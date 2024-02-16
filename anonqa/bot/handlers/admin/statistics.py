from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from ....shared.db.models import User
from ...filters.is_admin import IsAdmin

router = Router()


@router.message(IsAdmin(is_admin=True), Command(commands=["stats"]))
async def stats_handler(message: Message):
    count = await User.get_count()
    await message.answer(f"📊 <b>The number of bot users -</b> <code>{count}</code>")
