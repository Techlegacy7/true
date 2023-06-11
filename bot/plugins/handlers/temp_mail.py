from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from bot.config import Buttons
from bot.utils import get_mail, generate_mail, get_mailbox


@Client.on_message(
    filters.regex(f"^{Buttons.temp_mail_text}$") & filters.private & filters.incoming
)
async def temp_mail(bot: Client, message: Message):
    await message.reply_text(
        "Choose an option below:",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Generate Temporary Email",
                        callback_data="temp_mail",
                    ),
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("^temp_mail$"))
async def temp_mail_callback(bot: Client, callback_query: CallbackQuery):
    out = await callback_query.message.reply_text(
        "Generating temporary email...",
    )

    email = await generate_mail()

    await callback_query.message.reply_text(
        f"Here is your temporary email:\n\n`{email}`",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Check Inbox",
                        callback_data=f"check_inbox {email}",
                    ),
                ],
            ]
        ),
    )
    await out.delete()


@Client.on_callback_query(filters.regex("^check_inbox"))
async def check_inbox_callback(bot: Client, callback_query: CallbackQuery):
    email = callback_query.data.split()[1]

    try:
        mailbox = await get_mailbox(email)
    except Exception as e:
        print(e)
        await callback_query.answer(
            "Failed to check inbox or no emails found.",
            show_alert=True,
        )
        return

    if not mailbox:
        await callback_query.answer(
            "No emails found in your inbox.",
            show_alert=True,
        )
        return

    text = f"EMail: {email}\n\nFound {len(mailbox)} email(s) in your inbox.\n\nYour mails:\n\n"
    buttons = []
    for mail in mailbox:
        text += f"ID: `{mail['id']}`\nFrom: {mail['from']}\nSubject: {mail['subject']}\n\n"
        buttons.append(
            InlineKeyboardButton(
                f"{mail['id']}",
                callback_data=f"read_email {email} {mail['id']}",
            ),
        )

    buttons = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]

    buttons.append(
        [
            InlineKeyboardButton(
                "Refresh",
                callback_data=f"check_inbox {email}",
            ),
        ],
    )

    try:
        await callback_query.message.edit(
            text,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        await callback_query.answer()

    except Exception as e:
        print(e)
        await callback_query.answer("No new emails found in your inbox.")


@Client.on_callback_query(filters.regex("^read_email"))
async def read_email_callback(bot: Client, callback_query: CallbackQuery):
    email = callback_query.data.split()[1]
    _id = callback_query.data.split()[2]

    try:
        mail = await get_mail(email, _id)
    except Exception as e:
        print(e)
        await callback_query.answer(
            "Failed to fetch email.",
        )
        return

    text = (
        f"ID: `{mail['id']}`\nFrom: `{mail['from']}`\nSubject: `{mail['subject']}`\n\n"
    )
    text += f"Body: `{mail['textBody']}`\n\n"

    buttons = [
        [
            InlineKeyboardButton(
                "Back",
                callback_data=f"check_inbox {email}",
            ),
        ],
    ]

    await callback_query.message.edit(
        text,
        reply_markup=InlineKeyboardMarkup(buttons),
    )
