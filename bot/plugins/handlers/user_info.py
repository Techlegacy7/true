from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from bot.config import Buttons


@Client.on_message(filters.regex(f"^{Buttons.user_info_text}$"))
async def user_info(bot: Client, message: Message):
    await message.reply_text(
        "Choose an option below:",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "My Info", callback_data=f"user_info#{message.from_user.id}"
                    ),
                    InlineKeyboardButton(
                        "Other User Info", callback_data="user_info#0"
                    ),
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("^user_info#"))
async def user_info_callback(bot: Client, callback_query: CallbackQuery):
    asked_user_id = int(callback_query.data.split("#")[1])
    user_id = 0
    if asked_user_id == 0:
        ask: Message = await callback_query.message.chat.ask(
            "Forward any message from the user chat you want to get info about.",
        )
        if ask.forward_from:
            user_id = ask.forward_from.id
    else:
        user_id = asked_user_id

    if not user_id:
        await ask.reply_text("Wrong User ID / Username. Please try again.")
        return
    user = ask.forward_from if asked_user_id == 0 else callback_query.from_user
    user_info_text = f"""User ID: `{user.id}`
First Name: `{user.first_name}`
Last Name: `{user.last_name or 'None'}`
Mention: {user.mention}
Username: @{user.username or 'None'}
Status: `{user.status.value}`
"""
    await callback_query.message.reply_text(user_info_text)
