from pyrogram import Client, filters, types
from database import db
from bot.config import Config


@Client.on_message(
    filters.command("users") & filters.user(Config.ADMINS) & filters.incoming
)
async def users_count(bot, message: types.Message):
    total_users = await db.users.count_users()
    await message.reply_text(f"Total Users: {total_users}")
