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

import os

TOKEN = os.getenv("TOKEN")

updater: Updater = Updater(token=TOKEN)

dispatcher: Dispatcher = updater.dispatcher


def main():
    dispatcher.add_handler(handler=CommandHandler(command=('start'),callback=first))

    dispatcher.add_handler(handler=MessageHandler(filters=Filters.text('⛅️ Hozirgi ob-havo'),callback=hozir))
    dispatcher.add_handler(handler=MessageHandler(filters=Filters.location, callback=start))
    dispatcher.add_handler(handler=MessageHandler(filters=Filters.text('🕔 Soatlik ob-havo'),callback=hourly))
    # dispatcher.add_handler(handler=MessageHandler(Filters))
    dispatcher.add_handler(handler=MessageHandler(filters=Filters.text("📍 Hududni o'zgartirish"),callback=upd))
    dispatcher.add_handler(handler=MessageHandler(filters=Filters.text('📞 Aloqa'),callback=Aloqa))


    updater.start_polling()
    # stop the bot
    updater.idle()



if __name__ == "__main__":

    main()