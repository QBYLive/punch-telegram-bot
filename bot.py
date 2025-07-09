import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler

BOT_TOKEN = "7641013721:AAFmK69lAfZDDZGvEqPT3xPn0dblhBl9eZ4"
USERNAME = 7650968562  # Заміни на потрібний username
API_KEY = "qRptHWNir0haRqH5o3sVVe2XrOqtqi"
BALANCE_URL = f"https://daisysms.com/stubs/handler_api.php?api_key={API_KEY}&action=getBalance"

logging.basicConfig(level=logging.INFO)

# Отримуємо баланс
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

# Функція для автопінгу
import asyncio

async def auto_ping_balance(app):
    message = get_balance()
    await app.bot.send_message(chat_id=USER_CHAT_ID, text=f"📅 Автоперевірка о 10:00\n{message}")

# Команда /balance
async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = get_balance()
    await update.message.reply_text(message)

# Основна функція
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("balance", balance_command))

    # Розклад на 10:00 за Києвом
    from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler(timezone="Europe/Kiev")
scheduler.add_job(lambda: asyncio.create_task(auto_ping_balance(app)), 'cron', hour=10, minute=0)
scheduler.start()

    app.run_polling()

if __name__ == "__main__":
    main()
