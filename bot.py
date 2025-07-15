import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")
WEBHOOK_SECRET_KEY = os.getenv("WEBHOOK_SECRET_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text("Привет! Это NeoGPT, я запущен на Webhook с защитой!")

def main():
  app = Application.builder().token(BOT_TOKEN).build()
  
app.add_handler(CommandHandler("start", start))

# Запуск webhook-сервера с автоматическим set_webhook
app.run_webhook(
  listen="0.0.0.0",
  port=8000,
  webhook_path=f"/webhook/{BOT_TOKEN}",
  secret_token=WEBHOOK_SECRET_KEY,
  webhook_url=f"{BASE_URL}/webhook/{BOT_TOKEN}",
)

if __name__ == "__main__":
 main()
