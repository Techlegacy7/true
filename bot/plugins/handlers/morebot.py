import pyrogram
from bot.config import Buttons


@pyrogram.Client.on_message(
    pyrogram.filters.regex(pattern=f"^{Buttons.more_bot_regex}$")
    & pyrogram.filters.private
    & pyrogram.filters.incoming
)
async def more_bots_handler(bot, update):
    await update.reply_text("Checkout @BestBotsTG for more such amazing botsCheckout @BestBotsTG for more such amazing bots")
