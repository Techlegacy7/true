import random
import string
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from bot.config import Buttons

@Client.on_message(filters.regex(f"^{Buttons.strong_password_generator_text}$"))
async def pwd_generate(bot: Client, message: Message):
    await message.reply_text(
        "Choose an option below:",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Generate Password", callback_data="pwd_generate"
                    )
                ]
            ]
        ),
    )


@Client.on_callback_query(filters.regex("^pwd_generate$"))
async def pwd_generate_callback(bot: Client, callback_query: CallbackQuery):
    ask = await callback_query.message.chat.ask(
        "Enter the length of the password you want to generate.\n\n"
        "Note: The length should be between 8 and 32.\n\n"
        "Type /skip to set default length (8).",
    )

    if ask.text == "/skip":
        length = 8
    elif ask.text.isdigit():
        length = int(ask.text)
    else:
        await ask.reply_text(
            "Enter a valid number.\n" "Please try again.",
        )

    if length < 8 or length > 32:
        await ask.reply_text(
            "The length should be between 8 and 32.\n" "Please try again.",
        )
        return

    pwd = generate_password(length)

    await callback_query.message.reply_text(
        f"Your password is: `{pwd}`",
    )


def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(characters) for _ in range(length))
