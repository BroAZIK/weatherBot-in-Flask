from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
import requests
from pprint import pprint
import os
from tinydb import TinyDB, Query
from tinydb.table import Document

db = TinyDB('db.json',indent=4)



from details.buttons import (
    menu,
    location,
    upg_location
)

from details.messages import(
    Hozirgi_mes,
    Aloqa_mes
)





API_KEY = "28dc01ee165eb8b2d366fd571988a069"
URL = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
Hourly = "https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={lat}&lon={lon}&appid={API_KEY}"

def first(update: Update, context: CallbackContext):

    text = "Sizga ob-havoni ko'rsatishim uchun, Menga: lokatsiya yuboring! ⛔️"

    update.message.reply_html(
        text=text,
        reply_markup=ReplyKeyboardMarkup(location, resize_keyboard=True)
    )

def start(update: Update, context: CallbackContext):

    text = 'Kerakli buyruqni tanlang👇🏻'

    update.message.reply_html(
        text=text,
        reply_markup=ReplyKeyboardMarkup(menu, resize_keyboard=True)
    )

    chat_id = update.message.chat.id



    lat = update.message.location.latitude
    lon = update.message.location.longitude
    
    User = Query()


    result = db.search(User.chat_id==chat_id)

    if result != []:
        doc = Document(
            value = {"chat_id":chat_id,"lat":lat,"lon":lon},
            doc_id=chat_id
            )

        db.update(doc)

    else:

        doc = Document(
        value = {"chat_id":chat_id,"lat":lat,"lon":lon},
        doc_id=chat_id
        )

        db.insert(doc)

def hozir(update: Update, context: CallbackContext):


    chat_id = update.message.chat.id

    User = Query()

    result = db.search(User.chat_id==chat_id)

    print(result)

    lat = result[0]['lat']
    lon = result[0]['lon']

    print(lat, lon)

    print(result)

    url = URL.format(lat=lat, lon=lon, API_KEY=API_KEY)
    response = requests.get(url)
    data = response.json()


    pprint(data)

    shahar = data['name']

    osmon = data['weather'][0]['main']
    harorat1 = data['main']['temp']-273.15
    harorat = round(harorat1, 1)
    tuyuladi1 = data["main"]["feels_like"] - 273.15  
    tuyuladi = round(tuyuladi1, 1)

    bulutlar = data['clouds']['all'] 
    Namlik = data["main"]["humidity"]
    Shamol = data["wind"]["speed"]
    Bosim = data['main']['pressure']
    
    update.message.reply_text(
        text=Hozirgi_mes.format(shahar,osmon,harorat,tuyuladi,bulutlar,Namlik,Shamol,Bosim)
    )

def hourly(update: Update, context: CallbackContext):

    chat_id = update.message.chat.id

    User = Query()

    result = db.search(User.chat_id==chat_id)

    lat = result[0]['lat']
    lon = result[0]['lon']

    print(result)

    url = Hourly.format(lat=lat, lon=lon, API_KEY=API_KEY)
    response = requests.get(url)
    data = response.json()


    pprint(data)

def upd(update: Update, context: CallbackContext):


    update.message.reply_html(
        text="Yangi Joylashuvni Yuboring⚠️",
        reply_markup=ReplyKeyboardMarkup(upg_location,resize_keyboard=True)
    )

def after_upd(update: Update):

    text = 'Joylashuv Yangilandi✅'

    update.message.reply_html(
        text=text,
        reply_markup=ReplyKeyboardMarkup(menu, resize_keyboard=True)
    )

def Aloqa(update: Update, context: CallbackContext):

    first_name = update.effective_user.first_name

    update.message.reply_text(
        text=Aloqa_mes.format(first_name)
    )




TOKEN = "5809174742:AAHpxyhptxdSJUm4IOvNFWchEVWxttg5Nvg"

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