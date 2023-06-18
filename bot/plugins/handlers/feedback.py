import pyrogram

from bot.config import Buttons


@pyrogram.Client.on_message(
    pyrogram.filters.regex(pattern=f"^{Buttons.feedback_regex}$")
    & pyrogram.filters.private
    & pyrogram.filters.incoming
)
async def feedback_handler(bot, update):
    await update.reply_text("Feedback")
