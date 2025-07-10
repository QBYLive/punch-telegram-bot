import logging
import requests
import asyncio
import os

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler

# ==== Конфіг ====
BOT_TOKEN = os.getenv("BOT_TOKEN") or "7641013721:AAFmK69lAfZDDZGvEqPT3xPn0dblhBl9eZ4"
CHAT_ID = int(os.getenv("CHAT_ID") or 7650968562)  # Це ID користувача або групи
API_KEY = os.getenv("API_KEY") or "qRptHWNir0haRqH5o3sVVe2XrOqtqi"
BALANCE_URL = f"https://daisysms.com/stubs/handler_api.php?api_key={API_KEY}&action=getBalance"

logging.basicConfig(level=logging.INFO)

# ==== Отримання балансу ====
def get_balance():
    try:
        response = requests.get(BALANCE_URL)
        if "ACCESS_BALANCE" in response.text:
            balance = response.text.split(":")[1]
            return f"💰 Баланс акаунту: {balance}$"
        else:
            return "❌ Не вдалося отримати баланс. Перевір API ключ."
    except Exception as e:
        return f"⚠️ Помилка: {e}"

# ==== Асинхронна автоперевірка ====
async def auto_ping_balance(app):
    message = get_balance()
    try:
        await app.bot.send_message(chat_id=CHAT_ID, text=f"📅 Саме час показати баланс 🐧🫢\n{message}")
        logging.info("[✔] Автопінг: повідомлення надіслано.")
    except Exception as e:
        logging.error(f"[✖] Автопінг: помилка — {e}")

# ==== /balance команда ====
async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = get_balance()
    await update.message.reply_text(message)

# ==== /ping команда ====
async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = get_balance()
    try:
        await context.bot.send_message(chat_id=CHAT_ID, text=f"🔔 Ручний пінг активовано\n{message}")
        await update.message.reply_text("✅ Тестове повідомлення надіслано.")
        logging.info("[✔] Ручний пінг: повідомлення надіслано.")
    except Exception as e:
        await update.message.reply_text(f"❌ Помилка при надсиланні: {e}")
        logging.error(f"[✖] Ручний пінг: помилка — {e}")

# ==== Головна ====
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("balance", balance_command))
    app.add_handler(CommandHandler("ping", ping_command))

    scheduler = BackgroundScheduler(timezone="Europe/Kiev")
    scheduler.add_job(lambda: asyncio.run(auto_ping_balance(app)), trigger='cron', hour=10, minute=0)
    scheduler.start()

    logging.info("🚀 Бот запущено. Очікування команд...")
    app.run_polling()

if __name__ == "__main__":
    main()
