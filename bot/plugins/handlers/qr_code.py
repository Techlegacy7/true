import os
import pyrogram
from bot.utils import generate_qr_code
from bot.config import Buttons


@pyrogram.Client.on_message(
    pyrogram.filters.regex(pattern=f"^{Buttons.qr_code_text}$")
    & pyrogram.filters.private
    & pyrogram.filters.incoming
)
async def qr_code_handler(bot, update):
    text = "Send me the text you want to convert to QR code."

    ask = await update.chat.ask(text=text)

    if not ask.text:
        await ask.reply_text(text="You didn't send any text.")
        return
    out = await ask.reply_text(text="Generating QR code...")
    filename = f"downloads/{ask.id}_qr_code.png"
    try:
        qr_code = await generate_qr_code(ask.text, filename)
    except Exception as e:
        await ask.reply_text(text=f"Failed to generate QR code.\n\n**Error:** `{e}`")
        await out.delete()
        return
    await out.edit(text="Uploading QR code...")
    await ask.reply_document(
        document=qr_code,
        file_name="qr_code.png",
        caption="Here is the QR code for the text you sent.",
        quote=True,
    )

    os.remove(qr_code)
    await out.delete()
