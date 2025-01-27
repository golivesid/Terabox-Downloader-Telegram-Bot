import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram import executor
from decouple import config
from aiogram.types import InputFile
from time import monotonic
import speedtest
import subprocess

from func import *
from utils import *


def start_flask():
  clear()
  subprocess.Popen(["python3", "uptime.py"])


def update_bot():
  clear()
  subprocess.Popen(["python3", "update.py"])

logging.basicConfig(level=logging.INFO)

TOKEN = config('BOT_TOKEN', default='6845914467:AAGqfwYU5vZdRz-k5Fs6fhuXYJm_RH5E9tY')
APIKEY = config('APIKEY', default='23054736')
OWNER = config('OWNER', default='https://t.me/punjab_buy/')
CLEAN_TERMINAL = config('CLEAN_TERMINAL', default='False')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


async def on_startup(dp):
    commands = [
        types.BotCommand(command='start', description='Start the bot'),
        types.BotCommand(command='help', description='Get help'),
    ]
    await bot.set_my_commands(commands)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Hello! Send me video url to download video.\n\n Join Our Channel For New Updates @TERABOXSUPPORT01 ✔️")

@dp.message_handler(commands=['ping'])
async def ping(message: types.Message):
    start_time = monotonic()
    processing_message = await message.reply("Pinging....")
    end_time = monotonic()
    ping = int((end_time - start_time) * 1000)
    s = speedtest.Speedtest()
    servers = s.get_servers()
    download_speed = s.download() / 1000000
    upload_speed = s.upload() / 1000000
    url = s.results.share()
    caption = (f'▣ Ping : {ping} ms\n▣ Download : {download_speed:.2f} Mbit/s\n▣ Upload : {upload_speed:.2f} Mbit/s')
    await processing_message.delete()
    await bot.send_photo(message.chat.id, photo=url, caption=caption)
    
@dp.message_handler(commands=['stats'])
async def stats(message: types.Message):
    await message.reply(get_system_info())


@dp.message_handler()
async def echo(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    message_url = str(message.text)
    if CLEAN_TERMINAL:
        clear()
    await check_tmp()
    downloader = check_downloader(message_url)
    if downloader:
        processing_message = await message.reply("Please wait, downloading video!")
        try:
            video_info = await get_video_download_info(message_url, downloader, APIKEY)
            if video_info["status"]:
                file_path, size = await downloadFromUrl(video_info['url'])
                if file_path == False:
                    return await message.reply("Unable to download video! or Resend the Link🔗.")
                await processing_message.edit_text("Video download successful. Please wait, uploading your video 🍞.")
                with open(file_path, 'rb') as video_file:
                    await bot.send_chat_action(chat_id, "upload_video")
                    await bot.send_video(chat_id=message.chat.id, video=InputFile(video_file))
                    await processing_message.delete()
                    send_done = True
                    os.remove(file_path)
                    keyboard = types.InlineKeyboardMarkup()
                    url_button = types.InlineKeyboardButton(text="Author", url=OWNER)
                    url_button2 = types.InlineKeyboardButton(text="Channel", url="https://t.me/teraboxsupport01/")
                    keyboard.add(url_button, url_button2)
                    await message.reply("Thanks for using our bot⚕️.", reply_markup=keyboard)
            else:
                await message.reply('[-] Download Failed!')
        except Exception as e:
            print (e)
            await message.answer(f"Error: {str(e)}")
    else:
        print("[-] Unsupported URL")


if __name__ == '__main__':
    from aiogram import executor
    start_flask()
    update_bot ()
    clear ()
    executor.start_polling(dp, on_startup=on_startup)
