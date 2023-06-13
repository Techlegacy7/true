from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup
from bot.config import Script, Buttons
from bot.utils import add_new_user


@Client.on_message(filters.command("start") & filters.private & filters.incoming)
@Client.on_message(
    filters.regex(Buttons.main_menu_regex) & filters.private & filters.incoming
)
async def start(bot: Client, message: Message):
    await add_new_user(bot, message.from_user)
    await message.reply_text(
        Script.START_MESSAGE,
        disable_web_page_preview=True,
        quote=True,
        reply_markup=ReplyKeyboardMarkup(
            Buttons.START_BUTTONS, resize_keyboard=True, one_time_keyboard=False
        ),
    )
