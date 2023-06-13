import asyncio
import json
import logging
import os

import pyrogram
from PIL import Image
from pyrogram import enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.config import Config, Script, Buttons
from bot.utils import DownLoadFile, humanbytes


@pyrogram.Client.on_message(
    pyrogram.filters.regex(pattern=f"^{Buttons.video_downloader_text}$")
    & pyrogram.filters.private
    & pyrogram.filters.incoming
)
async def video_downloader(bot, update):
    supported_sites = """
Supported Sites

- YouTube
- Twitter
- Facebook
- Instagram
- Spotify
- Vimeo
- Dailymotion
- TikTok
- Likee
- Mashable
- TED"""
    await update.reply_text(
        f"Just send me any valid link to download the video\n{supported_sites}"
    )


@pyrogram.Client.on_message(
    pyrogram.filters.regex(pattern=".*http.*")
    & pyrogram.filters.private
    & pyrogram.filters.incoming
)
async def echo(bot, update):
    logging.info(update.from_user)
    url = update.text
    youtube_dl_username = None
    youtube_dl_password = None
    file_name = None

    if "|" in url:
        url_parts = url.split("|")
        if len(url_parts) == 2:
            url = url_parts[0]
            file_name = url_parts[1]
        elif len(url_parts) == 4:
            url = url_parts[0]
            file_name = url_parts[1]
            youtube_dl_username = url_parts[2]
            youtube_dl_password = url_parts[3]
        else:
            for entity in update.entities:
                if entity.type == enums.MessageEntityType.TEXT_LINK:
                    url = entity.url
                elif entity.type == enums.MessageEntityType.URL:
                    o = entity.offset
                    l = entity.length
                    url = url[o : o + l]
        if url is not None:
            url = url.strip()
        if file_name is not None:
            file_name = file_name.strip()
        # https://stackoverflow.com/a/761825/4723940
        if youtube_dl_username is not None:
            youtube_dl_username = youtube_dl_username.strip()
        if youtube_dl_password is not None:
            youtube_dl_password = youtube_dl_password.strip()
        logging.info(url)
        logging.info(file_name)
    else:
        for entity in update.entities:
            if entity.type == enums.MessageEntityType.TEXT_LINK:
                url = entity.url
            elif entity.type == enums.MessageEntityType.URL:
                o = entity.offset
                l = entity.length
                url = url[o : o + l]

    command_to_exec = [
        "yt-dlp",
        "--no-warnings",
        "--youtube-skip-dash-manifest",
        "-j",
        url,
    ]
    if youtube_dl_username is not None:
        command_to_exec.append("--username")
        command_to_exec.append(youtube_dl_username)
    if youtube_dl_password is not None:
        command_to_exec.append("--password")
        command_to_exec.append(youtube_dl_password)
    # logger.info(command_to_exec)
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    # logger.info(e_response)
    t_response = stdout.decode().strip()
    # logger.info(t_response)
    # https://github.com/rg3/youtube-dl/issues/2630#issuecomment-38635239
    if e_response and "nonnumeric port" not in e_response:
        # logger.warn("Status : FAIL", exc.returncode, exc.output)
        error_message = e_response.replace(
            "please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output.",
            "",
        )
        if "This video is only available for registered users." in error_message:
            error_message += Script.SET_CUSTOM_USERNAME_PASSWORD
        await bot.send_message(
            chat_id=update.chat.id,
            text=Script.NO_VOID_FORMAT_FOUND.format(str(error_message)),
            reply_to_message_id=update.id,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True,
        )
        return False
    # logger.info(response_json)
    inline_keyboard = []
    if t_response:
        # logger.info(t_response)
        x_reponse = t_response
        if "\n" in x_reponse:
            x_reponse, _ = x_reponse.split("\n")
        response_json = json.loads(x_reponse)
        save_ytdl_json_path = (
            f"{Config.DOWNLOAD_LOCATION}/{str(update.from_user.id)}.json"
        )
        with open(save_ytdl_json_path, "w", encoding="utf8") as outfile:
            json.dump(response_json, outfile, ensure_ascii=False)
        duration = response_json["duration"] if "duration" in response_json else None
        if "formats" in response_json:
            for formats in response_json["formats"]:
                format_id = formats.get("format_id")
                format_string = formats.get("format_note")
                if format_string is None:
                    format_string = formats.get("format")
                format_ext = formats.get("ext")
                approx_file_size = ""
                if "filesize" in formats:
                    approx_file_size = humanbytes(formats["filesize"])
                cb_string_video = f"video|{format_id}|{format_ext}"
                cb_string_file = f"file|{format_id}|{format_ext}"
                if format_string is not None and "audio only" not in format_string:
                    ikeyboard = [
                        InlineKeyboardButton(
                            f"S {format_string} video {approx_file_size} ",
                            callback_data=(cb_string_video).encode("UTF-8"),
                        ),
                        InlineKeyboardButton(
                            f"D {format_ext} {approx_file_size} ",
                            callback_data=(cb_string_file).encode("UTF-8"),
                        ),
                    ]
                else:
                    # special weird case :\
                    ikeyboard = [
                        InlineKeyboardButton(
                            "SVideo [" + "] ( " + approx_file_size + " )",
                            callback_data=(cb_string_video).encode("UTF-8"),
                        ),
                        InlineKeyboardButton(
                            "DFile [" + "] ( " + approx_file_size + " )",
                            callback_data=(cb_string_file).encode("UTF-8"),
                        ),
                    ]
                inline_keyboard.append(ikeyboard)
            if duration is not None:
                cb_string_64 = "audio|64k|mp3"
                cb_string_128 = "audio|128k|mp3"
                cb_string = "audio|320k|mp3"
                inline_keyboard.extend(
                    (
                        [
                            InlineKeyboardButton(
                                "MP3 " + "(" + "64 kbps" + ")",
                                callback_data=cb_string_64.encode("UTF-8"),
                            ),
                            InlineKeyboardButton(
                                "MP3 " + "(" + "128 kbps" + ")",
                                callback_data=cb_string_128.encode("UTF-8"),
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                "MP3 " + "(" + "320 kbps" + ")",
                                callback_data=cb_string.encode("UTF-8"),
                            )
                        ],
                    )
                )
        else:
            format_id = response_json["format_id"]
            format_ext = response_json["ext"]
            cb_string_file = f"file|{format_id}|{format_ext}"
            cb_string_video = f"video|{format_id}|{format_ext}"
            inline_keyboard.append(
                [
                    InlineKeyboardButton(
                        "SVideo", callback_data=(cb_string_video).encode("UTF-8")
                    ),
                    InlineKeyboardButton(
                        "DFile", callback_data=(cb_string_file).encode("UTF-8")
                    ),
                ]
            )
            cb_string_file = f"file={format_id}={format_ext}"
            cb_string_video = f"video={format_id}={format_ext}"
            inline_keyboard.append(
                [
                    InlineKeyboardButton(
                        "video", callback_data=(cb_string_video).encode("UTF-8")
                    ),
                    InlineKeyboardButton(
                        "file", callback_data=(cb_string_file).encode("UTF-8")
                    ),
                ]
            )
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        # logger.info(reply_markup)
        thumbnail = Config.DEF_THUMB_NAIL_VID_S
        thumbnail_image = Config.DEF_THUMB_NAIL_VID_S
        if "thumbnail" in response_json and response_json["thumbnail"] is not None:
            thumbnail = response_json["thumbnail"]
            thumbnail_image = response_json["thumbnail"]
        thumb_image_path = DownLoadFile(
            thumbnail_image,
            f"{Config.DOWNLOAD_LOCATION}/{str(update.from_user.id)}.webp",
            Config.CHUNK_SIZE,
            None,
            Script.DOWNLOAD_START,
            update.id,
            update.chat.id,
        )
        if os.path.exists(thumb_image_path):
            im = Image.open(thumb_image_path).convert("RGB")
            im.save(thumb_image_path.replace(".webp", ".jpg"), "jpeg")
        else:
            thumb_image_path = None
        await bot.send_message(
            chat_id=update.chat.id,
            text=Script.FORMAT_SELECTION.format(thumbnail)
            + "\n"
            + Script.SET_CUSTOM_USERNAME_PASSWORD,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML,
            reply_to_message_id=update.id,
        )
    else:
        cb_string_file = "file=LFO=NONE"
        cb_string_video = "video=OFL=ENON"
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    "SVideo", callback_data=(cb_string_video).encode("UTF-8")
                ),
                InlineKeyboardButton(
                    "DFile", callback_data=(cb_string_file).encode("UTF-8")
                ),
            ]
        )
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await bot.send_message(
            chat_id=update.chat.id,
            text=Script.FORMAT_SELECTION.format(""),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML,
            reply_to_message_id=update.id,
        )
