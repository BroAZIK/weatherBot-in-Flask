from telegram import Bot
TOKEN = "5809174742:AAGbE9O4S8BzeOjsy9Ycu4ibGld658Y8HcY"

bot = Bot(token=TOKEN)

def get_info():
    print(bot.get_webhook_info())


def delete():
    print(bot.delete_webhook())


def set():
    url = 'https://azizbek2007.pythonanywhere.com/webhook'
    print(bot.set_webhook(url=url))

set()