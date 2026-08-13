#!/bin/bash
echo "==> Setting up Telegram Bot Environment..."

# رفتن به پوشه اصلی
cd /var/www/html/ahmad/bot2

# نصب ابزارهای مورد نیاز سیستم در صورت عدم وجود
sudo apt update
sudo apt install -y python3 python3-venv python3-pip ffmpeg

# ساخت پوشه موقت
mkdir -p temp
chmod 777 temp

# ساخت محیط مجازی
python3 -m venv venv

# فعالسازی محیط مجازی و نصب کتابخانه ها
source venv/bin/activate
pip install -r requirements.txt

# کپی فایل تنظیمات اگر وجود نداشت
if [ ! -f .env ]; then
    cp .env.example .env
    echo "==> Created .env file. Please edit it with your real BOT_TOKEN!"
fi

echo "==> Setup completed successfully!"
echo "==> Now please run: sudo cp telegram-video-bot.service /etc/systemd/system/"
echo "==> And: sudo systemctl enable --now telegram-video-bot"
