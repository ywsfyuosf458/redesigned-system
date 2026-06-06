# =========================================================
# ULTIMATE TELEGRAM FILE BOT
# =========================================================
# المطور الرسمي : ابن المجزبي
# جميع الحقوق محفوظة © 2026
# =========================================================

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

# =========================================================
# CONFIG
# =========================================================

TOKEN = os.environ.get('BOT_TOKEN', '7799475779:AAHRy0s3jveFzhD2v6lnX-fneKWc9UHxSbk') # Modified to use environment variable



CHANNEL_USERNAME = "@REMXYUOSF99"

CHANNEL_LINK = "https://t.me/REMXYUOSF99"

TEMP_DIR = "temp"

# دعم ضغط فيديو حتى 300MB
MAX_VIDEO_SIZE = 300 * 1024 * 1024

# دعم فك ملفات حتى 2GB
MAX_ARCHIVE_SIZE = 2 * 1024 * 1024 * 1024

Path(TEMP_DIR).mkdir(exist_ok=True)

# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# =========================================================
# MEMORY
# =========================================================

user_sessions = {}

# =========================================================
# HELPERS
# =========================================================

def format_size(size):

    for unit in ["B", "KB", "MB", "GB", "TB"]:

        if size < 1024:
            return f"{size:.2f} {unit}"

        size /= 1024

async def safe_delete(path):

    try:

        if os.path.exists(path):

            if os.path.isdir(path):
                shutil.rmtree(path)

            else:
                os.remove(path)

    except:
        pass

async def run_cmd(command):

    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        raise Exception(stderr.decode())

# =========================================================
# SUB CHECK
# =========================================================

async def check_subscription(user_id, bot):

    try:

        member = await bot.get_chat_member(
            CHANNEL_USERNAME,
            user_id
        )

        return member.status in [
            "member",
            "administrator",
            "creator"
        ]

    except:

        return False

# =========================================================
# START
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    subscribed = await check_subscription(
        user_id,
        context.bot
    )

    if not subscribed:

        keyboard = [
            [
                InlineKeyboardButton(
                    "📢 الاشتراك بالقناة",
                    url=CHANNEL_LINK
                )
            ],
            [
                InlineKeyboardButton(
                    "✅ تحقق من الاشتراك",
                    callback_data="check_sub"
                )
            ]
        ]

        await update.message.reply_text(
            """
🚫 يجب الاشتراك بالقناة أولاً

بعد الاشتراك اضغط تحقق.

━━━━━━━━━━━━━━━

حقوق البوت © ابن المجزبي
            """,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return

    await update.message.reply_text(
        """
🎬 أهلاً بك في بوت ابن المجزبي الاحترافي

━━━━━━━━━━━━━━━

📌 المميزات:

✅ ضغط فيديو حقيقي
✅ ضغط PDF
✅ استخراج ZIP / RAR / 7Z / TAR
✅ دعم ملفات ضخمة
✅ استخراج MP3
✅ ضغط ذكي وعالي
✅ رفع الملف بعد المعالجة

━━━━━━━━━━━━━━━

📤 أرسل ملف للبدء
        """
    )

# =========================================================
# CHECK BUTTON
# =========================================================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    if query.data == "check_sub":

        subscribed = await check_subscription(
            query.from_user.id,
            context.bot
        )

        if subscribed:

            await query.edit_message_text(
                """
✅ تم التحقق بنجاح

📤 أرسل ملف للبدء

حقوق © ابن المجزبي
                """
            )

        else:

            await query.answer(
                "❌ لم تشترك بعد",
                show_alert=True
            )

# =========================================================
# RECEIVE FILE
# =========================================================

async def receive_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    subscribed = await check_subscription(
        user_id,
        context.bot
    )

    if not subscribed:

        await update.message.reply_text(
            "❌ اشترك بالقناة أولاً"
        )

        return

    document = update.message.document
    video = update.message.video

    file_obj = document or video

    if not file_obj:
        return

    file_name = file_obj.file_name or "file"

    size = file_obj.file_size

    ext = file_name.lower()

    user_sessions[user_id] = {
        "file_id": file_obj.file_id,
        "file_name": file_name
    }

    # =====================================================
    # VIDEO
    # =====================================================

    if video:

        if size > MAX_VIDEO_SIZE:

            await update.message.reply_text(
                "❌ أقصى حجم للفيديو 300MB"
            )

            return

        keyboard = [

            [
                InlineKeyboardButton(
                    "📉 ضغط قوي",
                    callback_data="video_low"
                )
            ],

            [
                InlineKeyboardButton(
                    "⚖️ ضغط متوسط",
                    callback_data="video_medium"
                )
            ],

            [
                InlineKeyboardButton(
                    "🎬 جودة عالية",
                    callback_data="video_high"
                )
            ]

        ]

        await update.message.reply_text(
            "🎛 اختر نوع ضغط الفيديو:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return

    # =====================================================
    # PDF
    # =====================================================

    if ext.endswith(".pdf"):

        keyboard = [
            [
                InlineKeyboardButton(
                    "📄 ضغط PDF",
                    callback_data="pdf"
                )
            ]
        ]

        await update.message.reply_text(
            "📄 اختر العملية:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return

    # =====================================================
    # ARCHIVES
    # =====================================================

    archives = [
        ".zip",
        ".rar",
        ".7z",
        ".tar",
        ".gz"
    ]

    if any(ext.endswith(a) for a in archives):

        if size > MAX_ARCHIVE_SIZE:

            await update.message.reply_text(
                "❌ الملف المضغوط أكبر من الحد."
            )

            return

        keyboard = [
            [
                InlineKeyboardButton(
                    "📦 فك الضغط",
                    callback_data="extract"
                )
            ]
        ]

        await update.message.reply_text(
            "📦 اختر العملية:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# =========================================================
# PROCESS
# =========================================================

async def process(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    user_id = query.from_user.id

    if user_id not in user_sessions:

        await query.edit_message_text(
            "❌ انتهت الجلسة"
        )

        return

    data = user_sessions[user_id]

    file = await context.bot.get_file(
        data["file_id"]
    )

    input_path = os.path.join(
        TEMP_DIR,
        data["file_name"]
    )

    await query.edit_message_text(
        "⬇️ جاري التحميل..."
    )

    await file.download_to_drive(input_path)

    ext = Path(input_path).suffix.lower()

    try:

        # =================================================
        # VIDEO COMPRESS
        # =================================================

        if query.data.startswith("video"):

            output = os.path.join(
                TEMP_DIR,
                f"compressed_{int(time.time())}.mp4"
            )

            if query.data == "video_low":

                crf = "35"

            elif query.data == "video_medium":

                crf = "28"

            else:

                crf = "22"

            await query.edit_message_text(
                "🎬 جاري ضغط الفيديو..."
            )

            command = [
                "ffmpeg",
                "-i", input_path,
                "-vcodec", "libx264",
                "-crf", crf,
                "-preset", "fast",
                "-movflags", "+faststart",
                "-y",
                output
            ]

            await run_cmd(command)

            await context.bot.send_video(
                chat_id=user_id,
                video=open(output, "rb"),
                caption="""
✅ تم ضغط الفيديو بنجاح

🤖 الحقوق © ابن المجزبي
                """
            )

            await safe_delete(output)

        # =================================================
        # PDF COMPRESS
        # =================================================

        elif query.data == "pdf":

            output = os.path.join(
                TEMP_DIR,
                f"compressed_{int(time.time())}.pdf"
            )

            await query.edit_message_text(
                "📄 جاري ضغط PDF..."
            )

            command = [
                "gs",
                "-sDEVICE=pdfwrite",
                "-dCompatibilityLevel=1.4",
                "-dPDFSETTINGS=/ebook",
                "-dNOPAUSE",
                "-dQUIET",
                f"-sOutputFile={output}",
                input_path
            ]

            await run_cmd(command)

            await context.bot.send_document(
                chat_id=user_id,
                document=open(output, "rb"),
                caption="""
✅ تم ضغط PDF

🤖 الحقوق © ابن المجزبي
                """
            )

            await safe_delete(output)

        # =================================================
        # EXTRACT FILES
        # =================================================

        elif query.data == "extract":

            extract_dir = os.path.join(
                TEMP_DIR,
                f"extract_{int(time.time())}"
            )

            os.makedirs(extract_dir, exist_ok=True)

            await query.edit_message_text(
                "📦 جاري فك الضغط..."
            )

            if ext == ".zip":

                with zipfile.ZipFile(input_path) as z:
                    z.extractall(extract_dir)

            elif ext == ".rar":

                with rarfile.RarFile(input_path) as r:
                    r.extractall(extract_dir)

       
            elif ext in [".tar", ".gz"]:

                with tarfile.open(input_path) as t:
                    t.extractall(extract_dir)

            output_zip = os.path.join(
                TEMP_DIR,
                f"extracted_{int(time.time())}.zip"
            )

            shutil.make_archive(
                output_zip.replace(".zip", ""),
                'zip',
                extract_dir
            )

            await context.bot.send_document(
                chat_id=user_id,
                document=open(output_zip, "rb"),
                caption="""
✅ تم فك الضغط بنجاح

🤖 الحقوق © ابن المجزبي
                """
            )

            await safe_delete(output_zip)
            await safe_delete(extract_dir)

        await query.edit_message_text(
            "✅ اكتملت العملية"
        )

    except Exception as e:

        logger.error(str(e))

        await query.edit_message_text(
            f"❌ خطأ:\n{str(e)[:300]}"
        )

    finally:

        await safe_delete(input_path)

        if user_id in user_sessions:
            del user_sessions[user_id]

# =========================================================
# MAIN
# =========================================================

def main():

    app = Application.builder().token(
        TOKEN # Modified to use the TOKEN variable
    ).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.Document.ALL | filters.VIDEO,
            receive_file
        )
    )

    app.add_handler(
        CallbackQueryHandler(buttons, pattern="check_sub")
    )

    app.add_handler(
        CallbackQueryHandler(process)
    )

    print("""
======================================================
 BOT STARTED SUCCESSFULLY
 Developer : ابن المجزبي
======================================================
""")

    app.run_polling()

# =========================================================

if __name__ == "__main__":
    main()
