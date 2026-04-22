import telebot
import requests
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    print("Error: No TOKEN in .env file!")
    exit()

bot = telebot.TeleBot(TOKEN)

# Add more coins here anytime (id from coingecko.com URL)
COIN_IDS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "XRP": "ripple",
    "BNB": "binancecoin",
    "ADA": "cardano",
    "DOGE": "dogecoin",
    "TRX": "tron",
    "AVAX": "avalanche-2",
    "SHIB": "shiba-inu",
}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🚀 Lightweight CoinGecko Price Bot ready!\nUse: /price BTC\nSupports: BTC ETH SOL XRP BNB ADA DOGE...")

@bot.message_handler(commands=['price'])
def get_price(message):
    try:
        symbol = message.text.split()[-1].upper().replace('/USDT', '').strip()
        if symbol not in COIN_IDS:
            bot.reply_to(message, f"❌ Unknown coin '{symbol}'. Try BTC, ETH, SOL etc.")
            return
        coin_id = COIN_IDS[symbol]
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true"
        data = requests.get(url, timeout=10).json()
        info = data[coin_id]
        price = info['usd']
        change = info.get('usd_24h_change', 0)
        vol = info.get('usd_24h_vol', 0)
        reply = f"📊 **{symbol}/USDT**\n💰 Price: ${price:,.4f}\n📈 24h Change: {change:+.2f}%\n📊 24h Vol: ${vol:,.0f}"
        bot.reply_to(message, reply, parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"❌ Error (maybe rate limit): {str(e)[:100]}")

print("🤖 Lightweight Bot is running... (Ctrl+C to stop)")
bot.polling(none_stop=True)
