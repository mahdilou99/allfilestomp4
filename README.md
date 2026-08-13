# Telegram TS to MP4 Converter Bot (@tstomp4Bot) 🎥

A high-performance Telegram bot that converts video files (like `.ts`, `.avi`, `.mov`, etc.) to `.mp4` format and makes them natively playable/streamable within Telegram. It bypasses Telegram's standard 20MB bot limit by utilizing a **Local Telegram Bot API Server**, allowing it to process files up to **2GB**.

---

## 🌟 Features
- **Bypass File Size Limits:** Handles files up to 2GB by running a Local Bot API server.
- **Ultra-Fast Conversion:** Uses FFmpeg `copy` codec (Stream Copy) for instant format changing without quality loss.
- **Smart Fallback:** If Stream Copy fails (due to incompatible codecs), it automatically falls back to full `H.264/AAC` re-encoding.
- **Native Telegram Playback:** Output files are sent as streamable videos, not raw documents.
- **Auto-Cleanup:** Deletes temporary files immediately after processing to save server disk space.

---

## 🛠️ Installation & Deployment (English)

This guide assumes you are deploying to an **Ubuntu** server.

### 1. Clone the Repository
```bash
git clone https://github.com/mahdilou99/allfilestomp4.git bot2
cd bot2
```

### 2. Run the Setup Script
This script installs required dependencies (FFmpeg, Python3, Venv) and creates the virtual environment.
```bash
chmod +x setup_ubuntu.sh
./setup_ubuntu.sh
```

### 3. Configure Environment Variables
Edit the generated `.env` file and insert your actual Bot Token.
```bash
nano .env
```
*(Leave `LOCAL_API_URL` as it is, unless you change the Docker port).*

### 4. Setup Local Telegram Bot API Server (Docker)
To allow 2GB files, you must run the Local Bot API Server. You'll need an `API_ID` and `API_HASH` from [my.telegram.org](https://my.telegram.org).

First, log out your bot from the cloud server (IMPORTANT):
```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/logOut"
```

Create a shared directory and run the Docker container:
```bash
sudo mkdir -p /var/lib/telegram-bot-api
sudo chown -R $USER:$USER /var/lib/telegram-bot-api

sudo apt install docker.io -y

sudo docker run -d -p 8042:8081 \
    --name=telegram-bot-api \
    --restart=always \
    -v /var/lib/telegram-bot-api:/var/lib/telegram-bot-api \
    -e TELEGRAM_API_ID="YOUR_API_ID" \
    -e TELEGRAM_API_HASH="YOUR_API_HASH" \
    -e TELEGRAM_LOCAL=1 \
    aiogram/telegram-bot-api:latest
```

### 5. Run the Bot as a Systemd Service
```bash
sudo cp telegram-video-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now telegram-video-bot
```
Check the status with: `sudo systemctl status telegram-video-bot`.

---
---

# ربات مبدل فرمت ویدیو به MP4 (@tstomp4Bot) 🇮🇷

این ربات یک ابزار قدرتمند برای تبدیل فایل‌های ویدیویی (مثل `ts`, `avi` و غیره) به فرمت `mp4` است تا به صورت مستقیم در تلگرام قابل پخش باشند. این ربات با استفاده از **Local Bot API Server** محدودیت ۲۰ مگابایتی تلگرام را دور زده و می‌تواند فایل‌های تا **۲ گیگابایت** را پردازش کند.

## 🌟 ویژگی‌ها
- **پشتیبانی از فایل‌های ۲ گیگابایتی:** دور زدن محدودیت‌های ربات تلگرام با سرور لوکال.
- **سرعت فوق‌العاده:** استفاده از قابلیت `Stream Copy` در FFmpeg برای تغییر فرمت در چند ثانیه بدون افت کیفیت.
- **تبدیل هوشمند (Fallback):** اگر فرمت ویدیو با کپی سازگار نباشد، ربات به صورت خودکار آن را به شکل کامل (H.264) تبدیل می‌کند.
- **پخش مستقیم در تلگرام:** ویدیوها به صورت Stream ارسال می‌شوند تا در خود تلگرام پخش شوند.
- **پاکسازی خودکار:** فایل‌های موقت پس از اتمام کار فوراً از سرور پاک می‌شوند.

---

## 🛠️ راهنمای نصب و راه‌اندازی روی سرور (فارسی)

مراحل زیر برای نصب روی سرور **اوبونتو (Ubuntu)** نوشته شده است.

### ۱. دریافت فایل‌ها از گیت‌هاب
```bash
git clone https://github.com/mahdilou99/allfilestomp4.git bot2
cd bot2
```

### ۲. اجرای اسکریپت نصب
این اسکریپت پیش‌نیازهایی مثل پایتون، FFmpeg و محیط مجازی را نصب می‌کند.
```bash
chmod +x setup_ubuntu.sh
./setup_ubuntu.sh
```

### ۳. تنظیم توکن ربات
فایل `.env` را باز کنید و توکن ربات خود را در آن قرار دهید:
```bash
nano .env
```

### ۴. اجرای سرور لوکال تلگرام (برای فایل‌های حجیم)
برای این مرحله به `API_ID` و `API_HASH` از سایت [my.telegram.org](https://my.telegram.org) نیاز دارید.

**بسیار مهم:** ابتدا ربات را از سرور اصلی تلگرام خارج کنید تا خطای حجم ندهد:
```bash
curl "https://api.telegram.org/bot<توکن_شما>/logOut"
```

سپس پوشه مشترک را ساخته و داکر را اجرا کنید:
```bash
sudo mkdir -p /var/lib/telegram-bot-api
sudo chown -R $USER:$USER /var/lib/telegram-bot-api

sudo apt install docker.io -y

sudo docker run -d -p 8042:8081 \
    --name=telegram-bot-api \
    --restart=always \
    -v /var/lib/telegram-bot-api:/var/lib/telegram-bot-api \
    -e TELEGRAM_API_ID="آی‌دی_شما" \
    -e TELEGRAM_API_HASH="هش_شما" \
    -e TELEGRAM_LOCAL=1 \
    aiogram/telegram-bot-api:latest
```

### ۵. اجرای نهایی ربات (سرویس دائمی)
```bash
sudo cp telegram-video-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now telegram-video-bot
```
برای بررسی وضعیت ربات می‌توانید دستور `sudo systemctl status telegram-video-bot` را وارد کنید.
