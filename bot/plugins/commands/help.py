from pyrogram import Client, filters
from pyrogram.types import Message
from bot.config import Script, Buttons


@Client.on_message(filters.command("help") & filters.private & filters.incoming)
@Client.on_message(
    filters.regex(Buttons.help_regex) & filters.private & filters.incoming
)
async def help(bot: Client, message: Message):
    await message.reply_text(
        Script.HELP_MESSAGE,
        disable_web_page_preview=True,
        quote=True,
    )
