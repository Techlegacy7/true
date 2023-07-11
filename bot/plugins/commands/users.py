from pyrogram import Client, filters, types
from database import db
from bot.config import Config

@Client.on_message(
    filters.command("users") & filters.user(Config.ADMINS) & filters.incoming
)
async def users_count(bot, message: types.Message):
    total_users = await db.users.col.count_documents({"is_group": False})
    total_groups = await db.users.col.count_documents({"is_group": True})

    await message.reply_text(
        f"Total Users: {total_users}\nTotal Groups: {total_groups}"
    )
