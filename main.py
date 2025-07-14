import telebot
import openai
import requests
import pymongo
from config import *

# Инициализация
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY
client = pymongo.MongoClient(MONGO_URL)
db = client["gpt_bot"]

# Приветствие
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋 Привет! Я — NeoGPT. Задай мне любой вопрос.")

# Ответ от GPT
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = str(message.from_user.id)

    # Сохраняем сообщение в базу
    db.messages.insert_one({
        "user_id": user_id,
        "message": message.text
    })

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message.text}]
        )
        reply = response['choices'][0]['message']['content']
        bot.send_message(message.chat.id, reply)

    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Ошибка: {e}")

# Запуск
if __name__ == "__main__":
    bot.infinity_polling()
