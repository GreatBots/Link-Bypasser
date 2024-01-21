import asyncio
from typing import Union
import logging
from pyrogram import Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_invite_link(bot: Client, chat_id: Union[str, int]):
    try:
        invite_link = await bot.create_chat_invite_link(chat_id=chat_id)
        return invite_link
    except FloodWait as e:
        logger.warning(f"Sleep of {e.value}s caused by FloodWait ...")
        await asyncio.sleep(e.value)
        return await get_invite_link(bot, chat_id)

async def handle_force_sub(bot: Client, cmd: Message):
    try:
        # Define your channel ID or username here
        channel_chat_id = -1002092798390  # Replace with your actual channel ID (use negative value for private channels)
        
        user = await bot.get_chat_member(chat_id=channel_chat_id, user_id=cmd.from_user.id)
        
        if user.status == "kicked":
            await bot.send_message(
                chat_id=cmd.from_user.id,
                text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/JoinOT).",
                disable_web_page_preview=True
            )
            return 400
    except UserNotParticipant:
        try:
            invite_link = await get_invite_link(bot, chat_id=channel_chat_id)
        except Exception as err:
            logger.error(f"Unable to do Force Subscribe to {channel_chat_id}\n\nError: {err}")
            return 200

        # Notify user to join the channel
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="**Please Join My Updates Channel to use this Bot!**\n\n"
                 "Due to Overload, Only Channel Subscribers can use the Bot!",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
                    ],
                    [
                        InlineKeyboardButton("🔄 Refresh 🔄", callback_data="refreshForceSub")
                    ]
                ]
            )
        )
        return 400
    except Exception as e:
        logger.error(f"Something went wrong: {e}")
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="Something went Wrong. Contact my [Support Group](https://t.me/JoinOT).",
            disable_web_page_preview=True
        )
        return 200
    return 200
