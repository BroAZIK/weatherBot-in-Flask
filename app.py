from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
import handlers
from dotenv import load_dotenv
import os

from telegram.ext import (
    Updater,
    CommandHandler,
    Dispatcher,
    MessageHandler,
    Filters
)
from handlers import(
    start,
    hozir,
    first,
    hourly,
    upd,
    Aloqa

)


load_dotenv()
TOKEN = os.environ.get('TOKEN')

print('TOKEN:', TOKEN)

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)


app = Flask(__name__)


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return "webhook is running...!"
    
    if request.method == 'POST':
        
        body = request.get_json()
        
        update = Update.de_json(body, bot)
        dispatcher.add_handler(handler=CommandHandler(command=('start'),callback=first))
        dispatcher.add_handler(handler=MessageHandler(filters=Filters.location, callback=start))

        dispatcher.add_handler(handler=MessageHandler(filters=Filters.text('⛅️ Hozirgi ob-havo'),callback=hozir))
        dispatcher.add_handler(handler=MessageHandler(filters=Filters.text('🕔 Soatlik ob-havo'),callback=hourly))        
        dispatcher.add_handler(handler=MessageHandler(filters=Filters.text("📍 Hududni o'zgartirish"),callback=upd))
        dispatcher.add_handler(handler=MessageHandler(filters=Filters.text('📞 Aloqa'),callback=Aloqa))

        dispatcher.process_update(update)

        return {'message': 'ok'}


if __name__ == '__main__':
    app.run(debug=True)