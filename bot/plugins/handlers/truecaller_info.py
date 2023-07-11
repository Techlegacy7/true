import re
import traceback
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.config import Buttons
from bot.utils import search_number
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

    txt = await message.reply_text("Searching for the number...")

    try:
        result = await search_number(ask.text)
    except Exception as e:
        await message.reply_text(f"Error: `{e}`")
        return

    try:
        data = result["data"][0]
        text = f"""Information found on Truecaller for {ask.text}:

Name: {data.get('name')}
Gender: {data.get('gender')}
Score: {data.get('score')}
Carrier: {data.get('phones', [{}])[0].get('carrier') if data.get('phones') else None}
Address: {data.get('addresses', [{}])[0].get('city') if data.get('addresses') else None} 
Email: {data.get('internetAddresses', [{}])[0].get('id') if data.get('internetAddresses') else None}
"""
        await txt.edit(text=text, disable_web_page_preview=True)
    except Exception as e:
        traceback.print_exc()
        await txt.edit(f"Error: `{e}`")


def html_to_markdown(html_content):
    converter = html2text.HTML2Text()
    converter.body_width = 0  # Set body_width to 0 to disable line wrapping
    return converter.handle(html_content)
