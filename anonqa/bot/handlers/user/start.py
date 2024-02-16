import binascii

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Message,
)

from ....shared import misc
from ....shared.config import Config
from ....shared.db.models import User
from ... import keyboards
from ...filters.is_admin import Dev

router = Router()


@router.message(Dev(), Command(commands=["start"]))
async def start_handler(message: Message, config: Config):
    user_id = message.from_user.id

    if not await User.is_registered(user_id):
        await User.register(user_id)

    if message.text != "/start":
        param = message.text.split(" ")[1]
        try:
            user = bytes.fromhex(param)
            assert len(user) == 32
        except (binascii.Error, AssertionError):
            await message.answer("❌ <b>Invalid parameter.</b>")
            return

        if not (user := await User.objects.get_or_none(user_hash=param)):
            await message.answer("❌ <b>Such user not found.</b>")
            return

        await message.answer(
            f"✉️ Click the button below to send a <u>truly anonymous</u> message to <b>{misc.get_name(user.user_id)}</b>.",
            reply_markup=keyboards.start.get_send_keyboard(param, config),
        )
        return

    await message.answer_animation(
        "https://t.me/hikari_assets/81",
        caption=(
            f"👋 <b>Hey there, {misc.get_name(user_id)}</b>. Yeah, this"
            " is your brand new <b>anonymous identity</b>.\n\nAre you tired of the bots,"
            " which provide pseudo-anonymous services? These bots, where you can pay"
            " to reveal the identity of the sender.\n\nWell then, you've come to the"
            " right place. <b>AnonQA</b> is a bot, which provides truly anonymous"
            " services. You can send messages to anyone, without revealing your"
            " identity.\n\nThis is your <b>inbox link</b>:\n"
            f"🔗 <code>https://t.me/AnonQA_robot?start={misc.get_hash(user_id)}</code>"
        ),
        reply_markup=keyboards.start.get_keyboard(),
    )


@router.inline_query(Dev(), F.query == "share")
async def share_handler(query: InlineQuery):
    await query.answer(
        results=[
            InlineQueryResultArticle(
                id="share",
                title="Send your inbox link",
                description="Click to send your inbox link to someone",
                input_message_content=InputTextMessageContent(
                    message_text=(
                        "📨 Here you can send me a <b>truly anonymous</b> message to me!"
                    ),
                    parse_mode="HTML",
                ),
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="📨 Send anonymous message",
                                url=f"https://t.me/AnonQA_robot?start={misc.get_hash(query.from_user.id)}",
                            )
                        ]
                    ]
                ),
            )
        ],
        cache_time=0,
    )
