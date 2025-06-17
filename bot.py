import telebot
import requests
import json

BOT_TOKEN = '7398067602:AAFDzaOwdl_n-R3zVKYkvDaY3cUFH8VlPeE'
CHANNEL_USERNAME = '@igDownloaderUpdates'
ADMIN_ID = 6411315434
FOOTER = "Powered by @SohilCodes"

bot = telebot.TeleBot(BOT_TOKEN)
users_file = "users.json"

# Save user
def save_user(user_id):
    try:
        with open(users_file, "r") as f:
            users = json.load(f)
    except:
        users = []

    if user_id not in users:
        users.append(user_id)
        with open(users_file, "w") as f:
            json.dump(users, f)

# Get user count
def get_user_count():
    try:
        with open(users_file, "r") as f:
            users = json.load(f)
        return len(users)
    except:
        return 0

# Force Join Check
def is_user_joined(chat_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, chat_id)
        return member.status in ['member', 'creator', 'administrator']
    except:
        return False

# Start Command
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if not is_user_joined(user_id):
        bot.send_message(user_id, f"🚫 पहले हमारे चैनल को जॉइन करें: {CHANNEL_USERNAME}\nफिर /start दबाएं।")
        return

    save_user(user_id)

    # Notify admin
    if user_id != ADMIN_ID:
        bot.send_message(ADMIN_ID, f"👤 New User Started Bot:\nName: {message.from_user.first_name}\nID: {user_id}")

    bot.send_message(user_id, "👋 स्वागत है! बस Instagram वीडियो या फोटो का लिंक भेजो और डाउनलोड करो।")

# Stats command (admin only)
@bot.message_handler(commands=['stats'])
def stats(message):
    if message.chat.id == ADMIN_ID:
        count = get_user_count()
        bot.send_message(ADMIN_ID, f"📊 Total Users: {count}")
    else:
        bot.send_message(message.chat.id, "❌ Access Denied")

# Broadcast command
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.chat.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ Access Denied")
        return

    msg = message.text.split("/broadcast ", 1)
    if len(msg) < 2:
        bot.send_message(ADMIN_ID, "⚠️ Usage: /broadcast Your message here")
        return

    text = msg[1]
    with open(users_file, "r") as f:
        users = json.load(f)

    success, failed = 0, 0
    for user in users:
        try:
            bot.send_message(user, text)
            success += 1
        except:
            failed += 1
    bot.send_message(ADMIN_ID, f"✅ Broadcast Done\nSuccess: {success} | Failed: {failed}")

# Instagram Downloader
@bot.message_handler(func=lambda m: True)
def downloader(message):
    user_id = message.chat.id
    if not is_user_joined(user_id):
        bot.send_message(user_id, f"🚫 पहले हमारे चैनल को जॉइन करें: {CHANNEL_USERNAME}")
        return

    url = message.text
    if "instagram.com" not in url:
        bot.send_message(user_id, "❌ कृपया एक वैध Instagram लिंक भेजें।")
        return

    bot.send_message(user_id, "⏳ डाउनलोड किया जा रहा है...")

    try:
        r = requests.post("https://saveig.app/api/ajaxSearch", data={"q": url}, headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})
        data = r.json()
        video_url = data['links'][0]['url']

        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("📥 Download Again", url=url))

        bot.send_video(user_id, video_url, caption=f"✅ डाउनलोड हो गया!\n\n{FOOTER}", reply_markup=markup)
    except Exception as e:
        print(e)
        bot.send_message(user_id, "❌ डाउनलोड में दिक्कत आई।")

bot.polling()
