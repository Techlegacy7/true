import asyncio
import logging
import math
import os
import time

import aiohttp
import contextlib
from aiohttp import web
from gtts import gTTS
from langdetect import LangDetectException, detect
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
import requests

from bot.config import Config
from database import db


async def start_webserver():
    routes = web.RouteTableDef()

    @routes.get("/", allow_head=True)
    async def root_route_handler(request):
        res = {
            "status": "running",
        }
        return web.json_response(res)

    async def web_server():
        web_app = web.Application(client_max_size=30000000)
        web_app.add_routes(routes)
        return web_app

    app = web.AppRunner(await web_server())
    await app.setup()
    await web.TCPSite(app, "0.0.0.0", 8000).start()
    logging.info("Web server started")


async def add_new_user(app, user):
    user_id = user.id
    if not await db.users.is_user_exist(user_id):
        await app.send_message(
            Config.LOG_CHANNEL, f"New user `{user_id}` ({user.mention}) joined the bot"
        )
        await db.users.add_user(user_id)
        logging.info(f"New user {user_id} added to database")
        return True


async def convert_text_to_speech(text, accent="us", filename="tts.mp3"):
    """
    Converts text to speech using the Google Text-to-Speech (gTTS) API.
    Args:
        text (str): The text to be spoken.
        accent (str): The TLD (top-level domain) code of the accent (default is 'us').
        filename (str): The filename to save the audio to (default is 'tts.mp3').

    Returns:
        filename
    """
    # Create the text-to-speech object with the desired language and accent
    try:
        language = detect(text)
    except LangDetectException:
        # Default to English if language detection fails
        language = "en"

    tts = gTTS(text=text, lang=language, tld=accent)
    await asyncio.to_thread(tts.save, filename)
    return filename


async def get_page_source(ph_no):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/114.0",
        "Referer": "https://www.findandtrace.com/trace-mobile-number-location",
    }
    url = "https://www.findandtrace.com/trace-mobile-number-location"
    data = {"mobilenumber": ph_no, "submit": "Trace"}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            source = await response.text()
            start = """<h1 style="font-size:18px;">Trace"""
            end = "Local time at phone location"
            return source[source.find(start) + len(start) : source.rfind(end)]


async def convert_text_to_pdf_with_image(text_file, output_pdf, photo=None):
    # Create a canvas with letter size
    c = canvas.Canvas(output_pdf, pagesize=letter)

    # Calculate the center position for the image
    image_width = 100
    image_height = 100
    image_x = (letter[0] - image_width) / 2
    image_y = letter[1] - 100 - image_height
    print(photo)
    if photo:
        # Draw the image at the center of the top of the page
        print(c.drawImage(
            ImageReader(photo), image_x, image_y, width=image_width, height=image_height
        ))

    # Set the font and size for the content
    c.setFont("Helvetica", 12)

    # Read the text file and add it to the canvas
    if os.path.exists(text_file):
        with open(text_file, "r") as file:
            text_content = file.read()
    else:
        text_content = text_file

    text_content = text_content.replace("\n", "<br/>")

    text_y = image_y - 20
    x = 20

    lines = text_content.split("<br/>")
    for line in lines:
        if text_y <= 50:
            # Add a new page if the remaining space is not enough for another line
            c.showPage()
            text_y = letter[1] - 50  # Adjust the starting y-position for the new page

        words = line.split()
        line_chunks = []
        current_chunk = words[0] if words else ""

        for word in words[1:]:
            temp_chunk = f"{current_chunk} {word}"
            if c.stringWidth(temp_chunk) < letter[0] - x * 2:
                current_chunk = temp_chunk
            else:
                line_chunks.append(current_chunk)
                current_chunk = word

        line_chunks.append(current_chunk)
        for chunk in line_chunks:
            c.drawString(x, text_y, chunk)
            text_y -= 20

    # Save the canvas to a PDF file
    c.save()


async def generate_mail():
    return requests.get(
        "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1"
    ).json()[0]


async def get_mailbox(email):
    mail = email.split("@")[0]

    domain = email.split("@")[1]

    return requests.get(
        f"https://www.1secmail.com/api/v1/?action=getMessages&login={mail}&domain={domain}"
    ).json()


async def get_mail(email, id):
    mail = email.split("@")[0]
    domain = email.split("@")[1]
    return requests.get(
        f"https://www.1secmail.com/api/v1/?action=readMessage&login={mail}&domain={domain}&id={id}"
    ).json()


async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        # if round(current / total * 100, 0) % 5 == 0:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \nP: {2}%\n".format(
            "".join(["█" for _ in range(math.floor(percentage / 5))]),
            "".join(["░" for _ in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2),
        )

        tmp = progress + "{0} of {1}\nSpeed: {2}/s\nETA: {3}\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            # elapsed_time if elapsed_time != '' else "0 s",
            estimated_total_time if estimated_total_time != "" else "0 s",
        )
        with contextlib.suppress(Exception):
            await message.edit(text=f"{ud_type}\n {tmp}")


def DownLoadFile(url, file_name, chunk_size, client, ud_type, message_id, chat_id):
    if os.path.exists(file_name):
        os.remove(file_name)
    if not url:
        return file_name
    r = requests.get(url, allow_redirects=True, stream=True)
    # https://stackoverflow.com/a/47342052/4723940
    total_size = int(r.headers.get("content-length", 0))
    downloaded_size = 0
    with open(file_name, "wb") as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                fd.write(chunk)
                downloaded_size += chunk_size
            if client is not None and ((total_size // downloaded_size) % 5) == 0:
                time.sleep(0.3)
                with contextlib.suppress(Exception):
                    client.edit_message_text(
                        chat_id,
                        message_id,
                        text=f"{ud_type}: {humanbytes(downloaded_size)} of {humanbytes(total_size)}",
                    )
    return file_name


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: " ", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        n += 1
    return f"{str(round(size, 2))} {Dic_powerN[n]}B"


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        (f"{str(days)}d, " if days else "")
        + (f"{str(hours)}h, " if hours else "")
        + (f"{str(minutes)}m, " if minutes else "")
        + (f"{str(seconds)}s, " if seconds else "")
        + (f"{str(milliseconds)}ms, " if milliseconds else "")
    )
    return tmp[:-2]
