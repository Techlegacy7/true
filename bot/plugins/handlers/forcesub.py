import contextlib
import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.errors import UserNotParticipant
from bot.config import Config

@Client.on_message(filters.private & filters.incoming)
async def forcesub(c: Client, m: Message):
    if Config.FORCE_SUB_CHANNEL:
        owner = await c.get_users(int(Config.OWNER_ID))
        invite_link = await c.create_chat_invite_link(Config.FORCE_SUB_CHANNEL)
        try:
            user = await c.get_chat_member(Config.FORCE_SUB_CHANNEL, m.from_user.id)
            if user.status == "kicked":
                await m.reply_text("**Hey you are banned 😜**", quote=True)
                return
        except UserNotParticipant:
            buttons = [
                [
                    InlineKeyboardButton(
                        text="Updates Channel 🔖", url=f"{invite_link.invite_link}"
                    )
                ]
            ]
            buttons.append([InlineKeyboardButton("🔄 Refresh", callback_data="refresh")])

            await m.reply_text(
                f"Hey {m.from_user.mention(style='md')} you need join My updates channel in order to use me 😉\n\n"
                "__Press the Following Button to join Now 👇__",
                reply_markup=InlineKeyboardMarkup(buttons),
                quote=True,
            )
            return
        except Exception as e:
            print(e)
            await m.reply_text(
                f"Something Wrong. Please try again later or contact {owner.mention(style='md')}",
                quote=True,
            )
            return
    await m.continue_propagation()


@Client.on_callback_query(filters.regex("^refresh"))
async def refresh_cb(c, m):
    owner = await c.get_users(int(Config.OWNER_ID))
    if Config.FORCE_SUB_CHANNEL:
        try:
            user = await c.get_chat_member(Config.FORCE_SUB_CHANNEL, m.from_user.id)
            if user.status == "kicked":
                with contextlib.suppress(Exception):
                    await m.message.edit("**Hey you are banned**")
                return
        except UserNotParticipant:
            await m.answer(
                "You are not yet joined our channel. First join and then press refresh button 🤤",
                show_alert=True,
            )
            return
        except Exception as e:
            print(e)
            await m.message.edit(
                f"Something Wrong. Please try again later or contact {owner.mention(style='md')}"
            )
            return

    await m.message.delete()
