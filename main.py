import telebot
from telebot import types
from flask import Flask, request
import threading

TOKEN = '7933020801:AAG2jwlFORScA2GAMr7b_aVdfeZH2KRBMWU'
ADMIN_ID = 6618449790

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

special_event_packages = {
    "پک هفتگی": {
        "price": "120,000 تومان",
        "desc": "پک هفتگی 100 ریشارژ حساب میشه و هر پک هفتگی وقتی می‌خرید 80 جم میده و روزانه 20 جم و 10 تا کریستال ارورا میده و حداکثر تا 10 تا می‌تونید همزمان خریداری کنید"
    },
    "279 جم (ایونت ویژه)": {
        "price": "309,000 تومان",
        "desc": "این بسته شامل 254 جم ریشارژ + 25 جم بونوس"
    },
    "2 پک هفتگی + 56 جم": {
        "price": "314,000 تومان",
        "desc": "این بسته 251 جم ریشارژ + 5 جم بونوس و در مجموع بعد دو هفته 440 جم از دو پک هفتگی + 56 جم که در مجموع 496 جم بهتون میده"
    },
    "3 پک هفتگی": {
        "price": "359,000 تومان",
        "desc": "این بسته شامل 300 جم ریشارژ و بعد 3 هفته در مجموع 660 جم میده بهتون"
    },
}

gem_packages = {
    "11 جم": {
        "price": "17,000 تومان",
        "desc": "این بسته شامل 10 جم ریشارژ + 1 جم بونوس"
    },
    "22 جم": {
        "price": "32,000 تومان",
        "desc": "این بسته شامل 20 جم ریشارژ + 2 جم بونوس"
    },
    "44 جم": {
        "price": "60,000 تومان",
        "desc": "این بسته شامل 40 جم ریشارژ + 4 جم بونوس"
    },
    "56 جم": {
        "price": "74,000 تومان",
        "desc": "این بسته شامل 51 جم ریشارژ + 5 جم لوتوس"
    },
    "86 جم": {
        "price": "99,000 تومان",
        "desc": "این بسته شامل 78 جم ریشارژ + 8 جم بونوس"
    },
    "108 جم": {
        "price": "135,000 تومان",
        "desc": "این بسته شامل 100 جم ریشارژ + 8 جم بونوس"
    },
    "228 جم": {
        "price": "273,000 تومان",
        "desc": "این بسته شامل 207 جم ریشارژ + 21 جم بونوس"
    },
    "279 جم": {
        "price": "309,000 تومان",
        "desc": "این بسته شامل 254 جم ریشارژ + 25 جم بونوس"
    },
    "پک هفتگی": {
        "price": "120,000 تومان",
        "desc": "پک هفتگی 100 ریشارژ حساب میشه و هر پک هفتگی وقتی می‌خرید 80 جم میده و روزانه 20 جم میده و حداکثر تا 10 تا می‌تونید همزمان خریداری کنید"
    },
    "بسته استارلایت301جم": {
        "price": "349,000 تومان",
        "desc": "این بسته برای خرید استارلایت بهترین گزینه می‌باشد"
    },
    "335 جم": {
        "price": "393,000 تومان",
        "desc": "این بسته شامل 305 جم ریشارژ + 30 جم بونوس"
    },
    "429 جم": {
        "price": "489,000 تومان",
        "desc": "این بسته شامل 390 جم ریشارژ + 39 جم بونوس"
    },
    "570 جم": {
        "price": "649,000 تومان",
        "desc": "این بسته شامل 519 جم ریشارژ + 51 جم بونوس"
    },
    "1028 جم": {
        "price": "1,169,000 تومان",
        "desc": "این بسته شامل 936 جم ریشارژ + 92 جم بونوس"
    },
    "2056 جم": {
        "price": "2,309,000 تومان",
        "desc": "این بسته شامل 1872 جم ریشارژ + 184 جم بونوس"
    },
}

user_states = {}

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("💎 خرید جم موبایل لجندز", "👤 حساب کاربری")  # دکمه‌ها در یک ردیف
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

@bot.message_handler(func=lambda m: m.text == "💎 خرید جم موبایل لجندز")
def show_packages(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🔥 بسته‌های ویژه ایونت")  # دکمه بسته ویژه
    pkgs = list(gem_packages.keys())
    for i in range(0, len(pkgs), 2):
        if i + 1 < len(pkgs):
            markup.row(pkgs[i], pkgs[i + 1])
        else:
            markup.row(pkgs[i])
    markup.row("بازگشت به منو")
    bot.send_message(message.chat.id, "📦 یکی از بسته‌های جم رو انتخاب کن:", reply_markup=markup)
@bot.message_handler(func=lambda m: m.text == "🔥 بسته‌های ویژه ایونت")
def show_special_event_packages(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for key in special_event_packages.keys():
        markup.row(key)
    markup.row("🔙 بازگشت به لیست بسته‌ها")
    bot.send_message(message.chat.id, "🔥 بسته‌های ویژه ایونت:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in gem_packages or m.text in special_event_packages)
def show_package_detail(message):
    if message.text in gem_packages:
        pkg = gem_packages[message.text]
    else:
        pkg = special_event_packages[message.text]

    text = f"🎁 <b>{message.text}</b>\n💰 قیمت: {pkg['price']}\nℹ️ {pkg['desc']}"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🛒 خرید")
    markup.row("🔙 بازگشت به لیست بسته‌ها")
    markup.row("بازگشت به منو")

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "🔙 بازگشت به لیست بسته‌ها")
def back_to_package_list(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🔥 بسته‌های ویژه ایونت")  # دکمه مخصوص رو باز برگردونیم
    pkgs = list(gem_packages.keys())
    for i in range(0, len(pkgs), 2):
        if i + 1 < len(pkgs):
            markup.row(pkgs[i], pkgs[i + 1])
        else:
            markup.row(pkgs[i])
    markup.row("بازگشت به منو")
    bot.send_message(message.chat.id, "📦 یکی از بسته‌های جم رو انتخاب کن:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "بازگشت به منو")
def back_to_menu(message):
    user_states.pop(message.chat.id, None)
    bot.send_message(message.chat.id, "بازگشت به منوی اصلی:", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "🛒 خرید")
def handle_buy(message):
    card_number = "6219861818197880"
    caption = (
        "تنها شماره کارت مجموعه موبایل لجندز آی‌آر\n\n"
        f"💳<code>{card_number}</code>💳\n\n"
        "💎 طارق نصاری جزیره 💎\n"
        "✅ بعد از واریز، عکس رسید + آیدی اکانت و آیدی سرور رو همینجا به صورت متن کنار عکس بفرستید."
    )
    bot.send_message(message.chat.id, caption, parse_mode="HTML")

@bot.message_handler(content_types=['photo'])
def handle_receipt_photo(message):
    # بررسی اینکه متن کنار عکس وجود داره یا نه
    if not message.caption:
        bot.reply_to(message, "⚠️ لطفا حتما آیدی تلگرام و آیدی سرور خودتون رو در کپشن عکس بفرستید.")
        return
    
    # ساخت متن ارسالی به ادمین
    user_id = message.chat.id
    user_name = message.from_user.first_name
    caption = message.caption
    
    text_to_admin = (
        f"📦 سفارش جدید\n"
        f"👤 کاربر: [{user_name}](tg://user?id={user_id})\n"
        f"🆔 آیدی کاربر: `{user_id}`\n"
        f"💬 آیدی و آیدی سرور:\n{caption}\n\n"
        f"💬 رسید پرداخت در عکس است."
    )
    
    markup = types.InlineKeyboardMarkup()
    callback_data = f"order_done_{user_id}"
    markup.add(types.InlineKeyboardButton("✅ انجام شد", callback_data=callback_data))
    
    bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=text_to_admin, parse_mode="Markdown", reply_markup=markup)
    bot.send_message(user_id, "✅ سفارش شما دریافت شد، بزودی شارژ خواهد شد.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("order_done_"))
def callback_order_done(call):
    user_id_str = call.data.replace("order_done_", "")
    try:
        user_id = int(user_id_str)
    except:
        bot.answer_callback_query(call.id, "خطا در شناسه کاربر.")
        return
    
    bot.send_message(user_id, "🎉 سفارش شما انجام شد. از خریدتون ممنونیم!")
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    bot.answer_callback_query(call.id, "سفارش به کاربر اطلاع داده شد.")

@bot.message_handler(func=lambda m: user_states.get(m.chat.id, {}).get('waiting_for_receipt') and m.content_type != 'photo')
def warn_invalid_receipt(message):
    bot.reply_to(message, "⚠️ لطفاً فقط عکس رسید پرداخت را ارسال کنید.")

@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(message.chat.id, "لطفاً از گزینه‌های موجود استفاده کن.", reply_markup=main_menu())

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
