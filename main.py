فایل نهایی کامل‌شده: ربات خرید جم با ذخیره شماره و پاداش و پروفایل

import telebot from telebot import types from flask import Flask, request import threading import sqlite3

TOKEN = '7933020801:AAG2jwlFORScA2GAMr7b_aVdfeZH2KRBMWU' ADMIN_ID = 6618449790 bot = telebot.TeleBot(TOKEN) app = Flask(name)

--- پایگاه داده ---

def init_db(): conn = sqlite3.connect('users.db') c = conn.cursor() c.execute(''' CREATE TABLE IF NOT EXISTS users ( user_id INTEGER PRIMARY KEY, phone TEXT, balance INTEGER DEFAULT 0, purchase_count INTEGER DEFAULT 0 ) ''') conn.commit() conn.close()

def add_or_update_user(user_id, phone): conn = sqlite3.connect('users.db') c = conn.cursor() c.execute(''' INSERT INTO users (user_id, phone) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET phone=excluded.phone ''', (user_id, phone)) conn.commit() conn.close()

def increase_user_reward(user_id, amount): conn = sqlite3.connect('users.db') c = conn.cursor() c.execute(''' UPDATE users SET balance = balance + ?, purchase_count = purchase_count + 1 WHERE user_id = ? ''', (amount, user_id)) conn.commit() conn.close()

def get_user_profile(user_id): conn = sqlite3.connect('users.db') c = conn.cursor() c.execute('SELECT phone, balance, purchase_count FROM users WHERE user_id=?', (user_id,)) row = c.fetchone() conn.close() if row: return { 'phone': row[0], 'balance': row[1], 'purchase_count': row[2] } return None

--- بسته‌ها ---

special_event_packages = { "پک هفتگی": { "price": "120,000 تومان", "desc": "پک هفتگی 100ریشارژ حساب میشه و هر پک هفتگی وقتی می‌خرید 80جم میده و روزانه 20جم و 10تا کریستال ارورا میده و حداکثر تا 10تا میتونید همزمان خریداری کنید", "پاداش": 2000 }, "279جم": { "price": "309,000 تومان", "desc": "این بسته شامل 254جم ریشارژ+25جم بونوس", "پاداش": 3000 }, "2پک هفتگی+56جم": { "price": "314,000 تومان", "desc": "این بسته 251جم ریشارژ+5 جم بونوس و در مجموع بعد دو هفته 440جم از دو پک هفتگی+56 جم که در مجموع 496 جم بهتون میده", "پاداش": 3000 }, "3پک هفتگی": { "price": "359,000 تومان", "desc": "این بسته شامل 300جم ریشارژ و بعد 3 هفته در مجموع 660 جم میده بهتون", "پاداش": 3000 } }

gem_packages = { "11جم": {"price": "17,000 تومان", "desc": "10جم ریشارژ+1جم بونوس", "پاداش": 1000}, "22جم": {"price": "32,000 تومان", "desc": "20جم ریشارژ+2جم بونوس", "پاداش": 1000}, "279جم": {"price": "309,000 تومان", "desc": "254جم ریشارژ+25جم بونوس", "پاداش": 3000}, "پک هفتگی": {"price": "120,000 تومان", "desc": "پک هفتگی شامل 80جم و کریستال ارورا", "پاداش": 2000}, "بسته استارلایت301جم": {"price": "349,000 تومان", "desc": "مناسب برای خرید استارلایت", "پاداش": 5000}, "335جم": {"price": "393,000 تومان", "desc": "305جم ریشارژ+30جم بونوس", "پاداش": 5000}, "429جم": {"price": "489,000 تومان", "desc": "390جم ریشارژ+39جم بونوس", "پاداش": 6000}, "570جم": {"price": "649,000 تومان", "desc": "519جم ریشارژ+51جم بونوس", "پاداش": 7000}, "1028جم": {"price": "1,169,000 تومان", "desc": "936جم ریشارژ+92جم بونوس", "پاداش": 10000}, "2056جم": {"price": "2,309,000 تومان", "desc": "1872جم ریشارژ+184جم بونوس", "پاداش": 16000} }

user_states = {}

def main_menu(): markup = types.ReplyKeyboardMarkup(resize_keyboard=True) markup.row("💎 خرید جم موبایل لجندز", "👤 حساب کاربری") return markup

@bot.message_handler(commands=['start']) def start(message): bot.send_message(message.chat.id, "به فروشگاه جم خوش اومدی!", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "👤 حساب کاربری") def profile(message): profile = get_user_profile(message.chat.id) if profile: text = f"📞 شماره: {profile['phone'] or 'ثبت نشده'}\n💰 پاداش: {profile['balance']:,} تومان\n🛒 خرید: {profile['purchase_count']} بار" else: text = "📛 حسابی ثبت نشده است." bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text == "💎 خرید جم موبایل لجندز") def list_packages(message): markup = types.ReplyKeyboardMarkup(resize_keyboard=True) markup.row("🔥 بسته‌های ویژه ایونت") for i, k in enumerate(gem_packages): markup.row(k) markup.row("بازگشت به منو") bot.send_message(message.chat.id, "📦 بسته موردنظر رو انتخاب کن:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🔥 بسته‌های ویژه ایونت") def show_event_packages(message): markup = types.ReplyKeyboardMarkup(resize_keyboard=True) for k in special_event_packages: markup.row(k) markup.row("بازگشت به منو") bot.send_message(message.chat.id, "🔥 انتخاب کن:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in gem_packages or m.text in special_event_packages) def show_package(message): pkg = gem_packages.get(message.text) or special_event_packages.get(message.text) text = f"💎 {message.text}\n💰 قیمت: {pkg['price']}\nℹ️ {pkg['desc']}\n🎁 پاداش: {pkg['پاداش']:,} تومان" user_states[message.chat.id] = {"selected_package": message.text} markup = types.ReplyKeyboardMarkup(resize_keyboard=True) markup.row("🛒 خرید", "بازگشت به منو") bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🛒 خرید") def ask_phone(message): markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True) markup.add(types.KeyboardButton("ارسال شماره تماس 📱", request_contact=True)) if message.chat.id in user_states: user_states[message.chat.id]["waiting_for_phone"] = True else: user_states[message.chat.id] = {"waiting_for_phone": True} bot.send_message(message.chat.id, "لطفاً شماره تماس خود را ارسال کنید:", reply_markup=markup)

@bot.message_handler(content_types=['contact']) def contact(message): phone = message.contact.phone_number user_id = message.chat.id add_or_update_user(user_id, phone) user_states.pop(user_id, None) bot.send_message(ADMIN_ID, f"📞 شماره از {message.from_user.first_name}: {phone}", parse_mode="Markdown") bot.send_message(user_id, "✅ شماره ذخیره شد. بعد از پرداخت عکس رسید را ارسال کنید.", reply_markup=main_menu())

@bot.message_handler(content_types=['photo']) def handle_photo(message): if not message.caption: bot.reply_to(message, "⚠️ لطفاً کپشن (آیدی + آیدی سرور) همراه عکس بفرستید.") return user_id = message.chat.id user_name = message.from_user.first_name text = f"📦 سفارش جدید از {user_name}\n🆔 آیدی: {user_id}\n📄 کپشن: {message.caption}" markup = types.InlineKeyboardMarkup() markup.add(types.InlineKeyboardButton("✅ انجام شد", callback_data=f"order_done_{user_id}")) bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=text, parse_mode="Markdown", reply_markup=markup) bot.send_message(user_id, "✅ سفارش شما دریافت شد، بزودی بررسی می‌شود.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("order_done_")) def callback_order_done(call): user_id = int(call.data.replace("order_done_", "")) selected = user_states.get(user_id, {}).get("selected_package") pkg = gem_packages.get(selected) or special_event_packages.get(selected) reward = pkg["پاداش"] if pkg else 0 if reward: increase_user_reward(user_id, reward) reward_msg = f"\n💰 {reward:,} تومان به حسابت افزوده شد." if reward else "" bot.send_message(user_id, f"✅ سفارش انجام شد.{reward_msg}") bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None) user_states.pop(user_id, None)

--- Flask webhook ---

@app.route('/', methods=['GET']) def index(): return 'Bot is running'

@app.route('/', methods=['POST']) def webhook(): update = telebot.types.Update.de_json(request.stream.read().decode("utf-8")) bot.process_new_updates([update]) return 'ok'

def run(): app.run(host='0.0.0.0', port=8080)

if name == 'main': init_db() threading.Thread(target=run).start() bot.infinity_polling()

