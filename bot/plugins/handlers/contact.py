import pyrogram
from bot.config import Buttons


@pyrogram.Client.on_message(
    pyrogram.filters.regex(pattern=f"^{Buttons.contact_regex}$")
    & pyrogram.filters.private
    & pyrogram.filters.incoming
)
async def contact_handler(bot, update):
    await update.reply_text("Contact")
