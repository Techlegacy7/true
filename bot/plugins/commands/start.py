from pyrogram import Client, filters, enums
from pyrogram.types import Message, ReplyKeyboardMarkup
from bot.config import Script, Buttons
from bot.utils import add_new_user

@Client.on_message(filters.command("start") & filters.incoming)
@Client.on_message(
    filters.regex(Buttons.main_menu_regex) & filters.private & filters.incoming
)
async def start(bot: Client, message: Message):
    is_group = message.chat.type in [
        enums.ChatType.GROUP,
        enums.ChatType.SUPERGROUP,
    ]
    await add_new_user(bot, message.chat if is_group else message.from_user, is_group)
    await message.reply_text(
        Script.START_MESSAGE,
        disable_web_page_preview=True,
        quote=True,
        reply_markup=ReplyKeyboardMarkup(
            Buttons.START_BUTTONS, resize_keyboard=True, one_time_keyboard=False
        ),
    )
