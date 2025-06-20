import ssl

# Tạm bỏ qua verify SSL (KHÔNG nên dùng lâu dài)
ssl._create_default_https_context = ssl._create_unverified_context
import os
import certifi
import snscrape.modules.twitter as sntwitter
import requests
import time

# ✅ Bắt Python sử dụng cert đúng
os.environ['SSL_CERT_FILE'] = certifi.where()

# ✅ Config Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ✅ Tên user Twitter cần theo dõi
TWITTER_USERNAME = "elonmusk"

# ✅ Biến tạm để lưu tweet cũ
last_tweet_id = None

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("❌ Telegram error:", e)

def get_latest_tweet():
    try:
        for tweet in sntwitter.TwitterUserScraper(TWITTER_USERNAME).get_items():
            return tweet
    except Exception as e:
        print("❌ Tweet fetch error:", e)
        return None

if __name__ == "__main__":
    print("✅ Bot started. Tracking:", TWITTER_USERNAME)
    while True:
        tweet = get_latest_tweet()
        if tweet:
            if tweet.id != last_tweet_id:
                last_tweet_id = tweet.id
                print(f"📢 New Tweet by @{TWITTER_USERNAME}: {tweet.content}")
                send_telegram(f"🧠 New tweet by <b>@{TWITTER_USERNAME}</b>:\n\n{tweet.content}")
        else:
            print("⚠️ Không lấy được tweet.")
        time.sleep(30)
