
import contextlib
from pyrogram import Client, filters, types
from pyrogram.errors import UserNotParticipant
from bot.config import Config


@Client.on_message(filters.private & filters.incoming)
async def forcesub_handler(c: Client, m: types.Message):

    owner = c.owner
    if Config.UPDATE_CHANNEL:
        invite_link = c.invite_link
        try:
            user = await c.get_chat_member(Config.UPDATE_CHANNEL, m.from_user.id)
            if user.status == "kicked":
                await m.reply_text("**Hey you are banned 😜**", quote=True)
                return
        except UserNotParticipant:
            buttons = [
                [
                    types.InlineKeyboardButton(
                        text="Updates Channel 🔖", url=invite_link.invite_link
                    )
                ]
            ]
            buttons.append(
                [types.InlineKeyboardButton(
                    "🔄 Refresh", callback_data="sub_refresh")]
            )

            await m.reply_text(
                f"Hey {m.from_user.mention(style='md')} you need join My updates channel in order to use me 😉\n\n"
                "Press the Following Button to join Now 👇",
                reply_markup=types.InlineKeyboardMarkup(buttons),
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


@Client.on_callback_query(filters.regex("sub_refresh"))
async def refresh_cb(c, m: types.CallbackQuery):
    owner = c.owner
    if Config.UPDATE_CHANNEL:
        try:
            user = await c.get_chat_member(Config.UPDATE_CHANNEL, m.from_user.id)
            if user.status == "kicked":
                with contextlib.suppress(Exception):
                    await m.message.edit("**Hey you are banned**")
                return
        except UserNotParticipant:
            await m.answer(
                "You have not yet joined our channel. First join and then press refresh button",
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
