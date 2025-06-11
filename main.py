import telebot
from telebot import types
from flask import Flask, request
import threading

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

password = "Tareq13731376"
uri = f"mongodb+srv://TareqGemBot:{password}@gemcluster.cjw8jid.mongodb.net/?retryWrites=true&w=majority&appName=Gemcluster"
client = MongoClient(uri, server_api=ServerApi('1'))

TOKEN = '7933020801:AAG2jwlFORScA2GAMr7b_aVdfeZH2KRBMWU'
ADMIN_ID = 6618449790

bot = telebot.TeleBot(TOKEN)

try:
    client.admin.command('ping')
    print("اتصال به MongoDB موفق بود!")
except Exception as e:
    print(f"خطا در اتصال به MongoDB: {e}")

db = client["GemMlbb"]
users_collection = db["users"]

# افزایش موجودی و تعداد خرید (معادل increase_user_reward)
def increase_user_reward(user_id, amount):
    users_collection.update_one(
        {"user_id": user_id},
        {"$inc": {"balance": amount, "purchase_count": 1}},
        upsert=True
    )

# افزودن یا آپدیت کاربر با شماره تلفن
def add_or_update_user(user_id, phone):
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"phone": phone}, "$setOnInsert": {"balance": 0, "purchase_count": 0}},
        upsert=True
    )

# دریافت پروفایل کاربر شامل شماره، موجودی و تعداد خریدها
def get_user_profile(user_id):
    user = users_collection.find_one({"user_id": user_id})
    if user:
        return {
            'phone': user.get('phone'),
            'balance': user.get('balance', 0),
            'purchase_count': user.get('purchase_count', 0)
        }
    return None

# دریافت شماره تلفن کاربر
def get_user_phone(user_id):
    user = users_collection.find_one({"user_id": user_id}, {"phone": 1})
    if user:
        return user.get('phone')
    return None

# گرفتن موجودی کاربر
def get_balance(user_id):
    user = users_collection.find_one({"user_id": user_id}, {"balance": 1})
    if user:
        return user.get("balance", 0)
    return 0

# نمایش موجودی کاربر
@bot.message_handler(commands=['balance'])
def show_balance(message):
    user_id = message.chat.id
    balance = get_balance(user_id)
    bot.send_message(user_id, f"موجودی شما: {balance} تومان")

# دستورات و هندلرها

user_states = {}
user_profiles = {}

# سایر کدهای شما برای بسته‌ها و منو بدون تغییر

special_event_packages = {
    "پک هفتگی": {
        "price": "120,000 تومان",
        "desc": "پک هفتگی 100ریشارژ حساب میشه و هر پک هفتگی وقتی می‌خرید 80جم میده و روزانه 20جم و 10تا کریستال ارورا میده و حداکثر تا 10تا میتونید همزمان خریداری کنید",
        "پاداش": 2000
    },
    "279جم": {
        "price": "309,000 تومان",
        "desc": "این بسته شامل 254جم ریشارژ+25جم بونوس",
        "پاداش": 3000
    },
    "2پک هفتگی+56جم": {
        "price": "314,000 تومان",
        "desc": "این بسته 251جم ریشارژ+5 جم بونوس و در مجموع بعد دو هفته 440جم از دو پک هفتگی+56 جم که در مجموع 496 جم بهتون میده",
        "پاداش": 3000
    },
    "3پک هفتگی": {
        "price": "359,000 تومان",
        "desc": "این بسته شامل 300جم ریشارژ و بعد 3 هفته در مجموع 660 جم میده بهتون",
        "پاداش": 3000
    }
}

gem_packages = {
    "11جم": {
        "price": "17,000 تومان",
        "desc": "این بسته شامل 10جم ریشارژ+1جم بونوس",
        "پاداش": 1000
    },
    "22جم": {
        "price": "32,000 تومان",
        "desc": "این بسته شامل 20جم ریشارژ+2جم بونوس",
        "پاداش": 1000
    },
    "44جم": {
        "price": "60,000 تومان",
        "desc": "این بسته شامل40جم ریشارژ+4جم بونوس",
        "پاداش": 1000
    },
    "56جم": {
        "price": "74,000 تومان",
        "desc": "این بسته شامل 51جم ریشارژ+5جم بونوس",
        "پاداش": 2000
    },
    "86جم": {
        "price": "99,000 تومان",
        "desc": "این بسته شامل78جم ریشارژ+8جم بونوس",
        "پاداش": 2000
    },
    "108جم": {
        "price": "135,000 تومان",
        "desc": "این بسته شامل 100جم ریشارژ+8 جم بونوس",
        "پاداش": 4000
    },
    "228جم": {
        "price": "273,000 تومان",
        "desc": "این بسته شامل 207 جم ریشارژ+ 21جم بونوس",
        "پاداش": 5000
    },
    "279جم": {
        "price": "309,000 تومان",
        "desc": "این بسته شامل 254جم ریشارژ+25جم بونوس",
        "پاداش": 3000
    },
    "پک هفتگی": {
        "price": "120,000 تومان",
        "desc": "پک هفتگی 100ریشارژ حساب میشه و هر پک هفتگی وقتی می‌خرید 80جم میده و روزانه 20جم و 10تا کریستال ارورا میده و حداکثر تا 10تا میتونید همزمان خریداری کنید",
        "پاداش": 2000
    },
    "بسته استارلایت301جم": {
        "price": "349,000 تومان",
        "desc": "این بسته برای خرید استارلایت بهترین گزینه می‌باشد",
        "پاداش": 5000
    },
    "335جم": {
        "price": "393,000 تومان",
        "desc": "این بسته شامل 305جم ریشارژ+30جم بونوس",
        "پاداش": 5000
    },
    "429جم": {
        "price": "489,000 تومان",
        "desc": "این بسته شامل 390جم ریشارژ+39جم بونوس",
        "پاداش": 6000
    },
    "570جم": {
        "price": "649,000 تومان",
        "desc": "این بسته شامل 519جم ریشارژ+51جم بونوس",
        "پاداش": 7000
    },
    "1028جم": {
        "price": "1,169,000 تومان",
        "desc": "این بسته شامل 936جم ریشارژ+92جم بونوس",
        "پاداش": 10000
    },
    "2056جم": {
        "price": "2,309,000 تومان",
        "desc": "این بسته شامل 1872جم ریشارژ+184جم بونوس",
        "پاداش": 16000
    },
}

def format_package_text(package_key):
    # ... (بدون تغییر، همینطور بمونه)
    if package_key in gem_packages:
        pkg = gem_packages[package_key]
    elif package_key in special_event_packages:
        pkg = special_event_packages[package_key]
    else:
        return "بسته یافت نشد."

    if package_key.isdigit():
        gem_label = f"{package_key}جم"
    else:
        gem_label = package_key

    text = (
        f"💎 {gem_label}\n"
        f"💰 قیمت: {pkg['price']}\n"
        f"ℹ️ {pkg['desc']}\n"
        f"🎁 پاداش خرید: {pkg['پاداش']:,} تومان"
    )
    return text

app = Flask(__name__)

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    if message.contact and user_states.get(message.chat.id, {}).get('waiting_for_phone'):
        phone = message.contact.phone_number
        user_id = message.chat.id
        add_or_update_user(user_id, phone)

        admin_msg = (
            f"📞 شماره تماس جدید از کاربر:\n"
            f"👤 [{message.from_user.first_name}](tg://user?id={user_id})\n"
            f"🆔 آیدی: `{user_id}`\n"
            f"📱 شماره: `{phone}`"
        )

        bot.send_message(ADMIN_ID, admin_msg, parse_mode="Markdown")

# ادامه‌ی کدهای منو و هندلرها (بدون تغییر)

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("💎 خرید جم موبایل لجندز", "👤 حساب کاربری")
    return markup

@app.route('/', methods=['GET'])
def index():
    return '✅ Bot is alive and running!', 200

@app.route('/', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "به فروشگاه جم خوش اومدی!\nیکی از گزینه‌ها رو انتخاب کن:", reply_markup=main_menu())

# ... بقیه‌ی هندلرهای مربوط به منو و بسته‌ها هم به همین شکل ادامه داشته باشند

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5000)).start()
    bot.infinity_polling()
