=========================================================


ULTIMATE TELEGRAM FILE BOT


=========================================================


المطور الرسمي : ابن المجزبي


جميع الحقوق محفوظة © 2026


=========================================================


import os
import time
import shutil
import zipfile
import rarfile
import tarfile
#import py7zr
import asyncio
import logging
import subprocess
from pathlib import Path
from telegram import (
Update,
InlineKeyboardButton,
InlineKeyboardMarkup
)
from telegram.ext import (
Application,
MessageHandler,
CallbackQueryHandler,
CommandHandler,
ContextTypes,
filters
)


=========================================================


CONFIG


=========================================================


TOKEN = os.environ.get('BOT_TOKEN', '7799475779:AAHRy0s3jveFzhD2v6lnX-fneKWc9UHxSbk')
CHANNEL_USERNAME = "@REMXYUOSF99"
CHANNEL_LINK = "https://t.me/REMXYUOSF99"
TEMP_DIR = "temp"


دعم ضغط فيديو حتى 300MB


MAX_VIDEO_SIZE = 300 * 1024 * 1024


دعم فك ملفات حتى 2GB


MAX_ARCHIVE_SIZE = 2 * 1024 * 1024 * 1024
Path(TEMP_DIR).mkdir(exist_ok=True)


=========================================================


LOGGING


=========================================================


logging.basicConfig(
level=logging.INFO,
format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


=========================================================


MEMORY


=========================================================


user_sessions = {}


=========================================================
