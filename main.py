import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
import threading

TOKEN = '7933020801:AAG2jwlFORScA2GAMr7b_aVdfeZH2KRBMWU'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# لیست بسته‌های جم
gem_packages = {
    "86 جم": {"price": "85,000 تومان", "desc": "مناسب برای خریدهای کوچک"},
    "172 جم": {"price": "160,000 تومان", "desc": "محبوب‌ترین بسته"},
    "257 جم": {"price": "230,000 تومان", "desc": "به‌صرفه برای پلیرهای فعال"},
}

# /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("💎 خرید جم Mobile Legends", callback_data="buy_gems"))
    bot.send_message(message.chat.id, "به فروشگاه جم خوش اومدی!\nبرای شروع یکی از گزینه‌ها رو انتخاب کن:", reply_markup=markup)

# انتخاب بسته
@bot.callback_query_handler(func=lambda call: call.data == "buy_gems")
def show_packages(call):
    markup = InlineKeyboardMarkup()
    for pkg_name in gem_packages:
        markup.add(InlineKeyboardButton(pkg_name, callback_data=f"pkg_{pkg_name}"))
    bot.edit_message_text("📦 یکی از بسته‌های جم رو انتخاب کن:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

# جزئیات بسته
@bot.callback_query_handler(func=lambda call: call.data.startswith("pkg_"))
def show_package_detail(call):
    pkg_name = call.data[4:]
    pkg = gem_packages.get(pkg_name, {})
    text = f"🎁 <b>{pkg_name}</b>\n💰 قیمت: {pkg['price']}\nℹ️ {pkg['desc']}"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🛒 خرید", callback_data=f"buy_{pkg_name}"))
    bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="HTML")

# Flask سرور ساده برای زنده نگه‌داشتن برنامه در Render
@app.route('/')
def index():
    return "✅ ربات با Polling در حال اجراست!"

# اجرای Flask در Thread جدا
def run_flask():
    app.run(host='0.0.0.0', port=10000)

# شروع Flask
threading.Thread(target=run_flask).start()

# شروع Polling
bot.infinity_polling()
