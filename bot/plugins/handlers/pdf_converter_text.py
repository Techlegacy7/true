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
    output_text = ""
    out = await message.reply_text("Send me a text / image you want to convert to PDF")

    while True:
        ask: Message = await message.chat.ask(
            text="Add more text / image to convert to PDF.\n\nSend /cancel to cancel.\nSend /done to finish.",
            timeout=3600,
        )

        if not ask.text and not ask.photo:
            await message.reply_text("It seems like you didn't send any text / image.")
            continue

        if ask.text == "/cancel":
            await message.reply_text("Cancelled!")
            return

        if ask.text == "/done":
            break

        if ask.text:
            output_text += ask.text
        else:
            temp = await ask.reply_text("Downloading...")
            photo_path = await ask.download(
                f"downloads/{message.chat.id}-{message.id}.jpg"
            )
            output_text += f"[Image]<img>{photo_path}</img>"
            await temp.delete()

        output_text += "\n"

    if not output_text:
        await message.reply_text("You didn't send any text / image.")
        return

    out = await message.reply_text("Converting to PDF...")

    text = output_text or ""
    path = f"downloads/{message.chat.id}-{message.id}.pdf"

    try:
        await convert_text_to_pdf_with_image(text, path)
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
