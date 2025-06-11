import telebot
from telebot import types
from flask import Flask, request
import threading
import sqlite3  # اضافه کن اینجا

# توابع دیتابیس
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            phone TEXT,
            balance INTEGER DEFAULT 0,
            purchase_count INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def increase_user_reward(user_id, amount):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        UPDATE users
        SET balance = balance + ?, purchase_count = purchase_count + 1
        WHERE user_id = ?
    ''', (amount, user_id))
    conn.commit()
    conn.close()

def get_user_profile(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT phone, balance, purchase_count FROM users WHERE user_id=?', (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            'phone': row[0],
            'balance': row[1],
            'purchase_count': row[2]
        }
    return None

def add_or_update_user(user_id, phone):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (user_id, phone) VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET phone=excluded.phone
    ''', (user_id, phone))
    conn.commit()
    conn.close()

def get_user_phone(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT phone FROM users WHERE user_id=?', (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return row[0]
    return None

TOKEN = '7933020801:AAG2jwlFORScA2GAMr7b_aVdfeZH2KRBMWU'
ADMIN_ID = 6618449790

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

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
    # ابتدا چک کن بسته تو دیکشنری‌های اصلی هست
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

user_states = {}
user_profiles = {}

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

    text = format_package_text(message.text)
    
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
@bot.message_handler(func=lambda m: m.text == "👤 حساب کاربری")
def show_profile(message):
    profile = get_user_profile(message.chat.id)
    if profile:
        text = (
            f"👤 پروفایل شما:\n"
            f"📞 شماره تماس: {profile['phone'] or 'ثبت نشده'}\n"
            f"💰 موجودی پاداش: {profile['balance']:,} تومان\n"
            f"🛒 تعداد خرید: {profile['purchase_count']}"
        )
    else:
        text = "شما هنوز اطلاعاتی ثبت نکرده‌اید."
    bot.send_message(message.chat.id, text, reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "🛒 خرید")
def handle_buy(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="ارسال شماره تماس 📱", request_contact=True)
    markup.add(button_phone)
    bot.send_message(message.chat.id, "لطفاً شماره تماس خود را برای تکمیل سفارش و دریافت پاداش ارسال کنید", reply_markup=markup)
    user_states[message.chat.id] = {'waiting_for_phone': True}
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    if message.contact is not None and user_states.get(message.chat.id, {}).get('waiting_for_phone'):
        phone = message.contact.phone_number
        user_id = message.chat.id
        add_or_update_user(user_id, phone)  # ذخیره شماره تو دیتابیس

        # بعد از ذخیره شماره، شماره کارت رو ارسال کن
        card_number = "6219861818197880"
        caption = (
            "تنها شماره کارت مجموعه موبایل لجندز آی‌آر\n\n"
            f"💳<code>{card_number}</code>💳\n\n"
            "💎 طارق نصاری جزیره 💎\n"
            "✅ بعد از واریز، عکس رسید + آیدی اکانت و آیدی سرور رو همینجا به صورت متن کنار عکس بفرستید."
        )
        bot.send_message(user_id, caption, parse_mode="HTML", reply_markup=main_menu())
        
        user_states.pop(user_id)  # حذف وضعیت انتظار

@bot.message_handler(content_types=['photo'])
def handle_receipt_photo(message):
    # بررسی اینکه متن کنار عکس وجود داره یا نه
    if not message.caption:
        bot.reply_to(message, "⚠️ لطفا آیدی و آیدی سرور خودتون رو در کپشن عکس بفرستید.")
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

if __name__ == '__main__':
    init_db()    
bot.infinity_polling()
