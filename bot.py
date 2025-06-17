import telebot
import requests

BOT_TOKEN = '7398067602:AAFDzaOwdl_n-R3zVKYkvDaY3cUFH8VlPeE'
CHANNEL_USERNAME = '@igDownloaderUpdates'
FOOTER = "Powered by @botusername"

bot = telebot.TeleBot(BOT_TOKEN)

# Force Join Check
def is_user_joined(chat_id):
    try:
        user = bot.get_chat_member(CHANNEL_USERNAME, chat_id)
        return user.status in ['member', 'creator', 'administrator']
    except:
        return False

# Start Command
@bot.message_handler(commands=['start'])
def start(message):
    if not is_user_joined(message.chat.id):
        bot.send_message(message.chat.id, f"🚫 पहले हमारे चैनल को जॉइन करें: {CHANNEL_USERNAME}\n\nजॉइन करने के बाद /start दबाएं।")
        return
    bot.send_message(message.chat.id, "👋 स्वागत है! बस कोई Instagram वीडियो या फोटो लिंक भेजो और डाउनलोड करो!")

# Instagram Downloader Handler
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    if not is_user_joined(message.chat.id):
        bot.send_message(message.chat.id, f"🚫 पहले हमारे चैनल को जॉइन करें: {CHANNEL_USERNAME}")
        return

    url = message.text
    if "instagram.com" not in url:
        bot.send_message(message.chat.id, "❌ कृपया एक वैध Instagram लिंक भेजें।")
        return

    bot.send_message(message.chat.id, "⏳ डाउनलोड किया जा रहा है...")

    try:
        api_url = "https://saveig.app/api/ajaxSearch"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        data = {
            "q": url
        }
        response = requests.post(api_url, headers=headers, data=data)
        result = response.json()
        video_url = result['links'][0]['url']

        bot.send_video(message.chat.id, video_url, caption=f"✅ डाउनलोड हो गया!\n\n{FOOTER}")
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "❌ डाउनलोड में कोई समस्या आई। कृपया दूसरा लिंक आज़माएं।")

bot.polling()
