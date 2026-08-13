import os
import asyncio
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# دریافت تنظیمات از متغیرهای محیطی
BOT_TOKEN = os.getenv("BOT_TOKEN")
LOCAL_API_URL = os.getenv("LOCAL_API_URL", "http://127.0.0.1:8081/bot")
LOCAL_API_FILE_URL = os.getenv("LOCAL_API_FILE_URL", "http://127.0.0.1:8081/file/bot")
TEMP_DIR = os.getenv("TEMP_DIR", "/var/www/html/ahmad/bot2/temp")

os.makedirs(TEMP_DIR, exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! لطفاً فایل ویدیویی خود را ارسال کنید تا آن را به .mp4 تبدیل کنم."
    )

async def convert_video_to_mp4(input_path: str, output_path: str) -> bool:
    """تبدیل سریع فایل‌های ویدیویی (شامل ts) به MP4"""
    # در اینجا از copy استفاده می‌کنیم تا بدون افت کیفیت و سریع کار کند
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-c", "copy",
        "-bsf:a", "aac_adtstoasc",
        output_path
    ]
    
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    _, stderr = await process.communicate()
    
    if process.returncode != 0:
        logger.error(f"FFmpeg Error: {stderr.decode()}")
        # اگر کپی ناموفق بود، سعی با تبدیل کامل:
        logger.info("Retrying with re-encoding...")
        cmd_fallback = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-c:v", "libx264",
            "-preset", "fast",
            "-c:a", "aac",
            output_path
        ]
        process2 = await asyncio.create_subprocess_exec(
            *cmd_fallback,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        _, stderr2 = await process2.communicate()
        if process2.returncode != 0:
             logger.error(f"FFmpeg Fallback Error: {stderr2.decode()}")
             return False
    return True

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # این هندلر برای document و video کار می‌کند
    message = update.message
    file_obj = message.document or message.video
    
    if not file_obj:
        return
        
    file_name = getattr(file_obj, 'file_name', 'video.ts')
    
    status_msg = await message.reply_text("⏳ در حال دریافت فایل...")
    
    base_name = os.path.splitext(file_name)[0]
    input_file = os.path.join(TEMP_DIR, f"{message.message_id}_{file_name}")
    output_file = os.path.join(TEMP_DIR, f"{message.message_id}_{base_name}.mp4")

    try:
        # دانلود فایل (تا سقف 2 گیگابایت به لطف سرور لوکال)
        # افزایش timeout به 3600 ثانیه (1 ساعت) برای فایل‌های حجیم ضروری است
        file = await context.bot.get_file(file_obj.file_id, read_timeout=3600, connect_timeout=3600)
        await file.download_to_drive(input_file)
        
        await status_msg.edit_text("⚙️ در حال پردازش و تبدیل فرمت به MP4...")
        
        # تبدیل فرمت
        success = await convert_video_to_mp4(input_file, output_file)
        
        if not success:
            await status_msg.edit_text("❌ خطایی در تبدیل فایل رخ داد. ممکن است فرمت فایل پشتیبانی نشود.")
            return

        await status_msg.edit_text("📤 در حال ارسال فایل MP4...")
        
        # ارسال فایل تبدیل شده به تلگرام
        with open(output_file, "rb") as video_stream:
            await message.reply_video(
                video=video_stream,
                caption="✅ فایل شما با موفقیت به MP4 تبدیل شد.",
                supports_streaming=True,
                read_timeout=3600,
                write_timeout=3600,
                connect_timeout=3600
            )
            
        await status_msg.delete()

    except Exception as e:
        logger.error(f"Error handling file: {e}")
        try:
            await status_msg.edit_text("❌ خطایی در پردازش درخواست شما رخ داد.")
        except:
            pass

    finally:
        # پاکسازی فایلهای موقت برای جلوگیری از پر شدن سرور
        for path in [input_file, output_file]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except OSError as e:
                    logger.error(f"Error removing {path}: {e}")

def main():
    if not BOT_TOKEN:
        raise ValueError("خطا: متغیر BOT_TOKEN در فایل .env یا محیط یافت نشد!")

    # تنظیم ربات برای استفاده از Local API Server
    # این بخش بسیار مهم است تا محدودیت‌های تلگرام برداشته شود
    app = Application.builder().token(BOT_TOKEN).base_url(LOCAL_API_URL).base_file_url(LOCAL_API_FILE_URL).local_mode(True).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.VIDEO, handle_document))
    
    logger.info("Bot is running with Local API Server...")
    app.run_polling()

if __name__ == "__main__":
    main()
