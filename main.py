import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask

TOKEN = '7933020801:AAHQWz8SWbuKDgqQDfNsnHNTxOf65Bo32JM'
bot = telebot.TeleBot(TOKEN)

# لیست بسته‌های جم (می‌تونی بعداً از دیتابیس یا فایل بخونی)
gem_packages = {
    "86 جم": {"price": "85,000 تومان", "desc": "مناسب برای خریدهای کوچک"},
    "172 جم": {"price": "160,000 تومان", "desc": "محبوب‌ترین بسته"},
    "257 جم": {"price": "230,000 تومان", "desc": "به‌صرفه برای پلیرهای فعال"},
}

# دستور شروع
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("💎 خرید جم Mobile Legends", callback_data="buy_gems"))
    bot.send_message(message.chat.id, "به فروشگاه جم خوش اومدی!\nبرای شروع یکی از گزینه‌ها رو انتخاب کن:", reply_markup=markup)

# هندلر انتخاب "خرید جم"
@bot.callback_query_handler(func=lambda call: call.data == "buy_gems")
def show_packages(call):
    markup = InlineKeyboardMarkup()
    for pkg_name in gem_packages:
        markup.add(InlineKeyboardButton(pkg_name, callback_data=f"pkg_{pkg_name}"))
    bot.edit_message_text("📦 یکی از بسته‌های جم رو انتخاب کن:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

# هندلر انتخاب بسته خاص
@bot.callback_query_handler(func=lambda call: call.data.startswith("pkg_"))
def show_package_detail(call):
    pkg_name = call.data[4:]
    pkg = gem_packages[pkg_name]
    text = f"🎁 <b>{pkg_name}</b>\n💰 قیمت: {pkg['price']}\nℹ️ {pkg['desc']}"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🛒 خرید", callback_data=f"buy_{pkg_name}"))
    bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="HTML")
# ======= اجرای ربات با Flask =======
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
