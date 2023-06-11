import os
import random
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from bot.config import Buttons
from bot.utils import convert_text_to_speech


@Client.on_message(filters.regex(f"^{Buttons.text_to_speech_text}$"))
async def text_to_speech(bot: Client, message: Message):
    await message.reply_text(
        "Choose an option below:",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Send Text",
                        callback_data="text_to_speech",
                    ),
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("^text_to_speech$"))
async def text_to_speech_callback(bot: Client, callback_query: CallbackQuery):
    ask = await callback_query.message.chat.ask(
        "Enter the text you want to convert to speech.\n\n"
        "Type /skip to set default text (Hello World).",
    )

    text = "Hello World" if ask.text == "/skip" else ask.text
    random_filename = "".join(random.choice("0123456789abcdef") for _ in range(32))
    out = await callback_query.message.reply_text(
        "Generating text to speech...",
    )
    audio = await convert_text_to_speech(text, filename=random_filename)

    await callback_query.message.reply_audio(
        audio,
        caption=f"Text to speech generated for: `{text[:1000]}`",
    )

    os.remove(audio)
    await out.delete()
