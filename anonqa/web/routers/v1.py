import base64
import json
from urllib.parse import parse_qsl, quote

import aiohttp
import structlog
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.web_app import check_webapp_signature
from fastapi import APIRouter, Depends, HTTPException, Request

from ...shared.db.models import User
from ...shared.misc import escape_html, get_hash_base, get_name
from ..bot import bot
from ..models import SendRequest, SendResponse

logger = structlog.get_logger(__name__)

router = APIRouter(
    prefix="/api/v1",
    tags=["v1"],
)


async def check_recaptcha_mw(
    request: Request,
    g_recaptcha_response: str,
) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": request.app.state.cfg.main.recaptcha_site_key,
                "response": g_recaptcha_response,
            },
        ) as response:
            if not (recaptcha_response := await response.json()).get("success"):
                await logger.debug(recaptcha_response)
                raise HTTPException(
                    status_code=400,
                    detail="Invalid recaptcha",
                )

    return g_recaptcha_response


@router.post(
    "/send",
    responses={
        500: {"description": "Internal server error"},
    },
    dependencies=[Depends(check_recaptcha_mw)],
)
async def send(request: Request, info: SendRequest) -> SendResponse:
    if not (
        user := await User.objects.get_or_none(
            user_hash=base64.b64decode(info.recipient_tag).hex()
        )
    ):
        raise HTTPException(status_code=404, detail="Such user not found")

    try:
        parsed_data = dict(parse_qsl(info.sender, strict_parsing=True))
        if not check_webapp_signature(request.app.state.cfg.main.token, info.sender):
            raise ValueError
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid sender",
        )

    try:
        user_id = json.loads(parsed_data["user"])["id"]
        name = get_name(user_id)

        await bot.send_message(
            user.user_id,
            (
                "📨 <b>You've got a new message from"
                f" {name}:</b>\n\n{escape_html(info.message)}"
            ),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="📨 Answer anonymously",
                            web_app=WebAppInfo(
                                url=f"{request.app.state.cfg.main.local_api_endpoint}/send?r={quote(get_hash_base(user_id))}"
                            ),
                        )
                    ],
                ]
            ),
        )
    except Exception:
        await logger.exception("Failed to send message")
        raise HTTPException(status_code=500, detail="Internal server error")

    try:
        await bot.send_message(
            user_id,
            (
                f"📨 <b>Your message has been delivered to {escape_html(get_name(user.user_id))}:</b>\n\n"
                f"{escape_html(info.message)}"
            ),
        )
    except Exception:
        await logger.exception("Failed to send message")
        raise HTTPException(status_code=500, detail="Internal server error")

    return SendResponse(
        status="success",
        message=f"Message to {get_name(user.user_id)} sent",
    )
