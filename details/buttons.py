from telegram import KeyboardButton




menu = [
    ['⛅️ Hozirgi ob-havo'],
    ['🕔 Soatlik ob-havo','🗓 Haftalik ob-havo'],
    ["📍 Hududni o'zgartirish"],
    ['📞 Aloqa']
    ]


location = [
        [
            KeyboardButton("Joylashuvni Yuborish📍", request_location=True),
        ],
    ] 

upg_location = [
    [
        KeyboardButton("Joylashuvni o'zgartitsh📍", request_location=True)
    ]
]