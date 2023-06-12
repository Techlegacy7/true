import os
import traceback
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.config import Buttons
from bot.utils import convert_text_to_pdf_with_image


@Client.on_message(
    filters.regex(f"^{Buttons.pdf_converter_text}$")
    & filters.private
    & filters.incoming
)
async def pdf_converter(bot: Client, message: Message):
    ask = await message.chat.ask(
        text="Send me the text / image you want to convert to PDF.",
        timeout=3600,
    )
    # check if the message contains text or photo
    if not ask.text and not ask.photo:
        await message.reply_text("Invalid input! Please try again.")
        return

    out = await message.reply_text("Converting to PDF...")

    if ask.text:
        text = ask.text
        photo = None
    else:
        text = None
        photo = ask.photo

    path = f"downloads/{message.chat.id}-{message.id}.pdf"

    try:
        await convert_text_to_pdf_with_image(text, path, photo)
    except Exception as e:
        traceback.print_exc()
        await message.reply_text("Something went wrong! Please try again.")
        return

    await message.reply_document(
        document=path,
        caption="Here is your PDF file.",
    )

    os.remove(path)
    await out.delete()