import telebot
from telebot import types
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

# 📌 منوی اصلی
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("💎 خرید جم Mobile Legends")
    return markup

# 🟢 start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "به فروشگاه جم خوش اومدی!\nیکی از گزینه‌ها رو انتخاب کن:", reply_markup=main_menu())

# 🛒 نمایش بسته‌ها
@bot.message_handler(func=lambda m: m.text == "💎 خرید جم Mobile Legends")
def show_packages(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for pkg_name in gem_packages:
        markup.row(pkg_name)
    markup.row("بازگشت به منو")
    bot.send_message(message.chat.id, "📦 یکی از بسته‌های جم رو انتخاب کن:", reply_markup=markup)

# ℹ️ جزئیات بسته
@bot.message_handler(func=lambda m: m.text in gem_packages)
def show_package_detail(message):
    pkg = gem_packages[message.text]
    text = f"🎁 <b>{message.text}</b>\n💰 قیمت: {pkg['price']}\nℹ️ {pkg['desc']}"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🛒 خرید")
    markup.row("بازگشت به منو")
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="HTML")

# ⬅️ بازگشت به منو
@bot.message_handler(func=lambda m: m.text == "بازگشت به منو")
def back_to_menu(message):
    bot.send_message(message.chat.id, "بازگشت به منوی اصلی:", reply_markup=main_menu())

# 👛 خرید (فعلاً فقط پاسخ می‌ده)
@bot.message_handler(func=lambda m: m.text == "🛒 خرید")
def handle_buy(message):
    payment_info = (
        "تنها شماره کارت مجموعه موبایل لجندز آی‌آر\n\n"
        "💳6219861818197880💳\n\n"
        "💎طارق نصاری جزیره 💎\n"
        "✅بعد از واریز عکس رسید واریزی + آیدی و آیدی سرور رو اینجا بفرستید ✅"
    )
    bot.send_message(message.chat.id, payment_info)
# 🛑 فالس بک برای متن‌های غیرقابل تشخیص
@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(message.chat.id, "لطفاً از گزینه‌های موجود استفاده کن.", reply_markup=main_menu())

from flask import Flask, request
import threading

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return '✅ Bot is alive and running!', 200

@app.route('/', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200

def run():
    app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run).start()

bot.infinity_polling()
