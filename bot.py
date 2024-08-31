import os
import logging
import telebot
import requests
import time

# Получаем токен Telegram и API ключ ProxyAPI из переменных окружения Railway
TELEGRAM_TOKEN = os.getenv('7510973135:AAGFsIT5cbx5qVoSnX1P8UVfgMmr_zNwpGM')
PROXY_API_KEY = os.getenv('sk-d95EU3k2JrHW0yfLrozNJSzsCqBvzYhF')
PROXY_API_URL = "https://api.proxyapi.ru/openai/v1/chat/completions"

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем объект бота
bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False)

# Функция для отправки запроса в ProxyAPI
def send_to_proxyapi(user_message):
    headers = {
        "Authorization": f"Bearer {PROXY_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_message}]
    }
    try:
        logger.info("Отправка запроса на ProxyAPI...")
        response = requests.post(PROXY_API_URL, headers=headers, json=data)
        response.raise_for_status()
        logger.info("Запрос к ProxyAPI выполнен успешно.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к ProxyAPI: {e}")
        raise

# Обработчик команды /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, использующий ProxyAPI для общения. Напиши мне что-нибудь!")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True, content_types=["text"])
def handle_message(message):
    user_message = message.text
    bot.reply_to(message, "Ваше сообщение принято, обрабатываю...")

    try:
        bot.reply_to(message, "Отправка запроса к ProxyAPI...")
        response = send_to_proxyapi(user_message)
        ai_response = response['choices'][0]['message']['content'].strip()
        bot.reply_to(message, f"Ответ от сервера: {ai_response}")
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка при обработке вашего сообщения.")
        logger.error(f"Ошибка при обработке сообщения: {e}")

# Запуск бота на определенное время
def main():
    bot.polling(timeout=30)  # Ожидание сообщений в течение 30 секунд
    time.sleep(10)  # Затем бот "засыпает" на 10 секунд перед завершением работы

if __name__ == "__main__":
    main()
