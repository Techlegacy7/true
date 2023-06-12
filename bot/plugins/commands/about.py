from pyrogram import Client, filters
from pyrogram.types import Message
from bot.config import Script, Buttons


@Client.on_message(filters.command("about") & filters.private & filters.incoming)
@Client.on_message(
    filters.regex(Buttons.about_regex) & filters.private & filters.incoming
)
async def about(bot: Client, message: Message):
    await message.reply_text(
        Script.ABOUT_MESSAGE,
        disable_web_page_preview=True,
        quote=True,
    )
