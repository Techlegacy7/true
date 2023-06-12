import re
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.config import Buttons
from bot.utils import get_page_source
import html2text

@Client.on_message(
    filters.regex(f"{Buttons.trucaller_info_text}") & filters.private & filters.incoming
)
async def truecaller_info(client: Client, message: Message):
    ask = await message.chat.ask(
        text="Send me the number you want to search for.\n\n"
        "Example: `+919876543210`\n"
        "Only Indian numbers are supported.\n\n",
        filters=filters.text,
        timeout=3600,
    )

    regex = r"^\+?[1-9]\d{1,14}$"

    if not re.search(regex, ask.text):
        await message.reply_text("Invalid number! Please try again.")
        return

    await message.reply_text("Searching for the number...")

    ph_no = ask.text.replace("+91", "")

    try:
        page_source = await get_page_source(ph_no)
    except Exception as e:
        await message.reply_text(f"Error: `{e}`")
        return
    page_source = html_to_markdown(page_source)
    # replace *, -, |, \n\n with empty string
    page_source = re.sub(r"[*\-\|#]", "", page_source)
    page_source = re.sub(r"\n\n", "\n", page_source)
    await message.reply_text(
        text=page_source,
        disable_web_page_preview=True,
    )

def html_to_markdown(html_content):
    converter = html2text.HTML2Text()
    converter.body_width = 0  # Set body_width to 0 to disable line wrapping
    return converter.handle(html_content)