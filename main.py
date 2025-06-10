import telebot
from telebot import types
from flask import Flask, request
import threading

TOKEN = '7933020801:AAG2jwlFORScA2GAMr7b_aVdfeZH2KRBMWU'
ADMIN_ID = 6618449790

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

gem_packages = {
    "86 جم": {"price": "85,000 تومان", "desc": "مناسب برای خریدهای کوچک"},
    "172 جم": {"price": "160,000 تومان", "desc": "محبوب‌ترین بسته"},
    "257 جم": {"price": "230,000 تومان", "desc": "به‌صرفه برای پلیرهای فعال"},
}

user_states = {}

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("💎 خرید جم Mobile Legends")
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

@bot.message_handler(func=lambda m: m.text == "💎 خرید جم Mobile Legends")
def show_packages(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for pkg_name in gem_packages:
        markup.row(pkg_name)
    markup.row("بازگشت به منو")
    bot.send_message(message.chat.id, "📦 یکی از بسته‌های جم رو انتخاب کن:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in gem_packages)
def show_package_detail(message):
    pkg = gem_packages[message.text]
    user_states[message.chat.id] = {'selected_package': message.text}
    text = f"🎁 <b>{message.text}</b>\n💰 قیمت: {pkg['price']}\nℹ️ {pkg['desc']}"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🛒 خرید")
    markup.row("بازگشت به منو")
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="HTML")

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
        "✅ بعد از واریز، عکس رسید + آیدی تلگرام خودتون + آیدی سرور رو همینجا به صورت متن کنار عکس بفرستید."
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
        f"💬 رسید پرداخت در عکس زیر است."
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
