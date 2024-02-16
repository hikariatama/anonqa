import base64
from urllib.parse import quote

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo


def get_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📨 Share your link",
                    switch_inline_query="share",
                )
            ]
        ]
    )


def get_send_keyboard(recipient: str, config) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📨 Send a message",
                    web_app=WebAppInfo(
                        url=f"{config.main.local_api_endpoint}/send?r={quote(base64.b64encode(bytes.fromhex(recipient)).decode())}"
                    ),
                )
            ],
        ]
    )
