# Don't Remove Credit Tg - https://t.me/roxybasicneedbot1
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@roxybasicneedbot
# Ask Doubt on telegram https://t.me/roxybasicneedbot1

import os
import re
import sys
import json
import time
import asyncio
import requests
import subprocess

import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN, FORCE_SUB_CHANNEL, FORCE_SUB_CHANNEL_LINK, ADMINS, OWNER_ID
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, UserNotParticipant, ChatAdminRequired
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.enums import ParseMode, ChatMemberStatus

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN)

WELCOME_IMAGE_PATH = "welcome.jpg"

async def is_subscribed(bot, user_id):
    if not FORCE_SUB_CHANNEL:
        return True
    try:
        member = await bot.get_chat_member(chat_id=FORCE_SUB_CHANNEL, user_id=user_id)
        if member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
            return True
        else:
            return False
    except UserNotParticipant:
        return False
    except Exception as e:
        print(f"Error checking subscription: {e}")
        return False

# FIXED DECORATOR: Ab joined users ko reply milega
def force_subscribe(func):
    async def wrapper(client, message, *args, **kwargs):
        if FORCE_SUB_CHANNEL:
            is_sub = await is_subscribed(client, message.from_user.id)
            if not is_sub:
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔔 Join Channel", url=FORCE_SUB_CHANNEL_LINK)],
                    [InlineKeyboardButton("🔄 Refresh", callback_data="refresh_sub")]
                ])
                await message.reply_text(
                    f"<b>🔒 Access Denied!</b>\n\nYou must join our channel to use this bot.\n\n👇 Click the button below to join:",
                    reply_markup=keyboard,
                    parse_mode=ParseMode.HTML
                )
                return
        return await func(client, message, *args, **kwargs)
    return wrapper

def is_valid_url(url):
    url_pattern = re.compile(r'^https?://', re.IGNORECASE)
    return url_pattern.match(url) is not None

def extract_url_from_line(line):
    line = line.strip()
    if not line: return None, None
    url_match = re.search(r'https?://[^\s]+', line)
    if url_match:
        url = url_match.group()
        title = line.replace(url, '').strip() or f"File_{hash(url) % 1000}"
        return title, url
    return None, None

@bot.on_message(filters.command(["start"]))
@force_subscribe
async def start(bot: Client, m: Message):
    welcome_text = f"<b>👋 Hello {m.from_user.mention}!</b>\n\n<blockquote>📁 I am a bot for downloading files from your <b>.TXT</b> file and uploading them to Telegram.\n\n🚀 To get started, send /upload command and follow the steps.</blockquote>"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚡ Upload Files", callback_data="upload_files")],
        [
            InlineKeyboardButton("🔔 Channel", url="https://whatsapp.com/channel/0029VbBwIXh002TCXWoza60Y"),
            InlineKeyboardButton("👨‍💻 Developer", url="@Pandey_ji_up43_bot")
        ]
    ])
    if os.path.exists(WELCOME_IMAGE_PATH):
        await m.reply_photo(photo=WELCOME_IMAGE_PATH, caption=welcome_text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    else:
        await m.reply_text(welcome_text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

@bot.on_callback_query()
async def callback_handler(bot: Client, query: CallbackQuery):
    if query.data == "refresh_sub":
        is_sub = await is_subscribed(bot, query.from_user.id)
        if is_sub:
            await query.message.delete()
            await bot.send_message(query.from_user.id, "✅ **Subscription Verified!** Send /start to begin.")
        else:
            await query.answer("❌ Please join the channel first!", show_alert=True)
    elif query.data == "upload_files":
        await query.answer("Send /upload command to start!", show_alert=True)

@bot.on_message(filters.command(["upload"]))
@force_subscribe
async def upload(bot: Client, m: Message):
    editable = await m.reply_text('📤 Send your TXT file with links ⚡️')
    input_msg = await bot.listen(editable.chat.id)
    x = await input_msg.download()
    await input_msg.delete(True)

    try:
        with open(x, "r", encoding='utf-8', errors='ignore') as f:
            content = f.read()
        lines = content.split("\n")
        links = [[t, u] for line in lines for t, u in [extract_url_from_line(line)] if t and u]
        os.remove(x)
        if not links:
            await editable.edit("❌ No valid links found!")
            return
    except Exception as e:
        await editable.edit(f"❌ Error: {e}")
        return
    
    await editable.edit(f"📊 Total Links: {len(links)}\n\n📝 Send starting number:")
    input0 = await bot.listen(editable.chat.id)
    count = int(input0.text) if input0.text.isdigit() else 1
    await input0.delete(True)

    await editable.edit("📝 Enter batch name:")
    input1 = await bot.listen(editable.chat.id)
    batch_name = input1.text
    await input1.delete(True)
    
    await editable.edit("🎬 Select quality (144, 240, 360, 480, 720, 1080):")
    input2 = await bot.listen(editable.chat.id)
    qual = input2.text
    await input2.delete(True)
    
    await editable.edit("💬 Enter caption:")
    input3 = await bot.listen(editable.chat.id)
    caption_text = input3.text
    await input3.delete(True)
    
    await editable.edit("🖼 Send thumb URL or 'no':")
    input4 = await bot.listen(editable.chat.id)
    thumb_url = input4.text
    await input4.delete(True)
    await editable.delete()

    thumb = "no"
    if thumb_url.startswith("http"):
        getstatusoutput(f"wget '{thumb_url}' -O 'thumb.jpg'")
        thumb = "thumb.jpg" if os.path.exists("thumb.jpg") else "no"

    for i in range(count - 1, len(links)):
        try:
            title, url = links[i]
            name1 = re.sub(r'[<>:"/\\|?*]', '', title)[:50]
            name = f'{str(count).zfill(3)}) {name1}'
            
            prog = await bot.send_message(m.chat.id, f"⬇️ Downloading: `{name1}`")
            
            # Simple yt-dlp command
            cmd = f'yt-dlp -f "b[height<={qual}]/str" "{url}" -o "{name}.%(ext)s"'
            subprocess.run(cmd, shell=True)
            
            filename = None
            for ext in ['.mp4', '.mkv', '.pdf']:
                if os.path.exists(f"{name}{ext}"):
                    filename = f"{name}{ext}"
                    break
            
            if filename:
                if filename.endswith(".pdf"):
                    await bot.send_document(m.chat.id, filename, caption=f"**{name1}**\n{caption_text}")
                else:
                    await helper.send_vid(bot, m, f"**{name1}**\n{caption_text}", filename, thumb, name, prog)
                os.remove(filename)
            
            await prog.delete()
            count += 1
        except Exception:
            continue

if __name__ == "__main__":
    bot.run()
        
