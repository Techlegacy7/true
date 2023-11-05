import os
from dotenv import load_dotenv
from pyrogram import types
load_dotenv()


def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default


class Config(object):
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "tg_bot")
    DATABASE_URL = os.environ.get("DATABASE_URL", 'mongodb+srv://Lovely:Lovely@cluster0.fsid0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    OWNER_ID = int(os.environ.get("OWNER_ID"))
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0"))

    # optional
    FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1002076420040"))
    ADMINS = (
        list(map(int, os.environ.get("ADMINS").split()))
        if os.environ.get("ADMINS")
        else []
    )
    ADMINS.append(OWNER_ID) if OWNER_ID not in ADMINS else []
    WEB_SERVER = is_enabled(os.environ.get("WEB_SERVER", "False"), False)
    DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_DIR", "downloads")
    DEF_THUMB_NAIL_VID_S = os.environ.get("DEF_THUMB_NAIL_VID_S", "")
    CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 128))
    TG_MAX_FILE_SIZE = 2097152000
    DEF_WATER_MARK_FILE = os.environ.get("DEF_WATER_MARK_FILE", "")
    PROCESS_MAX_TIMEOUT = int(os.environ.get("PROCESS_MAX_TIMEOUT", 3600))


class Script(object):
    START_MESSAGE = "Choose an option from below:"
    HELP_MESSAGE = """Help Message"""
    ABOUT_MESSAGE = """<b>➥ My Name:</b> <code>Telegram Bot</code>"""
    SET_CUSTOM_USERNAME_PASSWORD = """If you want to download premium videos, provide in the following format:
URL | filename | username | password"""
    NO_VOID_FORMAT_FOUND = "ERROR...\n<b>YouTubeDL</b> said: {}"
    DOWNLOAD_START = "Now Downloading.."
    FORMAT_SELECTION = "Select the desired format: <a href='{}'>file size might be approximate</a> \nIf you want to set custom thumbnail, send photo before or quickly after tapping on any of the below buttons.\nYou can use /deletethumbnail to delete the auto-generated thumbnail."
    CANCEL_STR = "Process Cancelled"
    UPLOAD_START = "Now Uploading.."
    ZIP_UPLOADED_STR = "Uploaded {} files in {} seconds"
    CUSTOM_CAPTION_UL_FILE = "{}"
    RCHD_TG_API_LIMIT = "Downloaded in {} seconds.\nDetected File Size: {}\nSorry. But, I cannot upload files greater than 2GB due to Telegram API limitations."
    AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS = (
        "Downloaded in {} seconds.\nUploaded in {} seconds."
    )
    SLOW_URL_DECED = "Gosh that seems to be a very slow URL. Since you were screwing my home, I am in no mood to download this file."


class Buttons(object):
    user_info_text = "User Info"
    trucaller_info_text = "𝙏𝙧𝙪𝙚𝙘𝙖𝙡𝙡𝙚𝙧 𝙄𝙣𝙛𝙤 📞"
    strong_password_generator_text = "Strong Password Generator"
    video_downloader_text = "Video Downloader"
    temp_mail_text = "Temp Mail"
    qr_code_text = "QR Code"
    text_to_speech_text = "Text To Speech"
    pdf_converter_text = "PDF Converter"
    main_menu_regex = "Main Menu"
    help_regex = "Help"
    about_regex = "About"
    feedback_regex = "𝙈𝙤𝙫𝙞𝙚𝙨 📽️"
    movies_regex = "Movies"
    contact_regex = "Contact"
    more_bot_regex = "𝙈𝙤𝙧𝙚 𝘽𝙤𝙩𝙨 🤖"

    start_button_data = [
        [trucaller_info_text],
        # [strong_password_generator_text, video_downloader_text],
        #[temp_mail_text, qr_code_text],
       # [text_to_speech_text, pdf_converter_text],
        #[help_regex, about_regex],
       # [movies_regex, contact_regex],
        [feedback_regex, more_bot_regex],
    ]

    START_BUTTONS = [
        [types.KeyboardButton(button) for button in row] for row in start_button_data
    ]
