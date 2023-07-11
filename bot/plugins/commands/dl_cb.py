import contextlib
import os
import shutil
import time
import pyrogram

from bot.config import Config
from bot.config import Script as Translation
from bot.plugins.handlers.ddl_button import ddl_call_back
from bot.plugins.handlers.youtube_dl_button import youtube_dl_call_back
from bot.utils import progress_for_pyrogram


@pyrogram.Client.on_callback_query(pyrogram.filters.regex(r"^(file|video|audio)"))
async def button(bot, update):
    # logger.info(update)
    cb_data = update.data
    if ":" in cb_data:
        # unzip formats
        extract_dir_path = (
            f"{Config.DOWNLOAD_LOCATION}/{str(update.from_user.id)}zipped/"
        )
        if not os.path.isdir(extract_dir_path):
            await bot.delete_messages(
                chat_id=update.message.chat.id,
                message_ids=update.message.id,
                revoke=True,
            )
            return False
        zip_file_contents = os.listdir(extract_dir_path)
        type_of_extract, index_extractor, undefined_tcartxe = cb_data.split(":")
        if index_extractor == "NONE":
            with contextlib.suppress(Exception):
                shutil.rmtree(extract_dir_path)
            await bot.edit_message_text(
                chat_id=update.message.chat.id,
                text=Translation.CANCEL_STR,
                message_id=update.message.id,
            )
        elif index_extractor == "ALL":
            i = 0
            for file_content in zip_file_contents:
                current_file_name = os.path.join(extract_dir_path, file_content)
                start_time = time.time()
                await bot.send_document(
                    chat_id=update.message.chat.id,
                    document=current_file_name,
                    # thumb=thumb_image_path,
                    caption=file_content,
                    # reply_markup=reply_markup,
                    reply_to_message_id=update.message.id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        update.message,
                        start_time,
                    ),
                )
                i = i + 1
                os.remove(current_file_name)
            with contextlib.suppress(Exception):
                shutil.rmtree(extract_dir_path)
            await bot.edit_message_text(
                chat_id=update.message.chat.id,
                text=Translation.ZIP_UPLOADED_STR.format(i, "0"),
                message_id=update.message.id,
            )
        else:
            file_content = zip_file_contents[int(index_extractor)]
            current_file_name = os.path.join(extract_dir_path, file_content)
            start_time = time.time()
            await bot.send_document(
                chat_id=update.message.chat.id,
                document=current_file_name,
                # thumb=thumb_image_path,
                caption=file_content,
                # reply_markup=reply_markup,
                reply_to_message_id=update.message.id,
                progress=progress_for_pyrogram,
                progress_args=(
                    Translation.UPLOAD_START,
                    update.message,
                    start_time,
                ),
            )
            with contextlib.suppress(Exception):
                shutil.rmtree(extract_dir_path)
            await bot.edit_message_text(
                chat_id=update.message.chat.id,
                text=Translation.ZIP_UPLOADED_STR.format("1", "0"),
                message_id=update.message.id,
            )
    elif "|" in cb_data:
        await youtube_dl_call_back(bot, update)
    elif "=" in cb_data:
        await ddl_call_back(bot, update)
