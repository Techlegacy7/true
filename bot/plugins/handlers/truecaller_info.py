import re
import traceback
from pyrogram import Client, filters, types
from pyrogram.types import Message
from bot.config import Buttons
from bot.utils import search_number
import html2text
import json
@Client.on_message(
    filters.regex(f"{Buttons.trucaller_info_text}") & filters.private & filters.incoming
)
async def truecaller_info(client: Client, message: Message):
    ask = await message.chat.ask(
        text="Send me the number you want to search for.\n\n"
        "Example (Format): +919876543210\n"
        "Only Indian numbers are supported.\n\n",
        filters=filters.text,
        timeout=3600,
    )
    print(ask)
    regex = r"^\+?[1-9]\d{1,14}$"

    if not re.search(regex, ask.text):
        await message.reply_text("Invalid number! Please try again and see the example.")
        return

    txt = await message.reply_text("Searching for the number...")

    try:
        result = await search_number(ask.text)
    except Exception as e:
        await message.reply_text(f"Error : `{e}`")
        return
    try:
        Score = float(result["data"]["data"][0]["score"])
        score_Percent = Score*100
        text = f"""Information found on Truecaller for {ask.text}:
        
Name: {result["data"]["data"][0]["name"]}
Score: {score_Percent}%
Carrier: {result["data"]["data"][0]["phones"][0]["carrier"] if result["data"]["data"][0]["phones"] else None}
Address: {result["data"]["data"][0]["addresses"][0]["city"] if result["data"]["data"][0]["addresses"] else None} 
Email: {result["data"]["data"][0]["internetAddresses"][0]["id"] if result["data"]["data"][0]["internetAddresses"] else None}
"""
        await txt.edit(text=text, disable_web_page_preview=True)
    except Exception as e:
        traceback.print_exc()
        await txt.edit(f"Error: {e}")


def html_to_markdown(html_content):
    converter = html2text.HTML2Text()
    converter.body_width = 0  # Set body_width to 0 to disable line wrapping
    return converter.handle(html_content)
