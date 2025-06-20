import snscrape.modules.twitter as sntwitter
import requests
import time

# === Config ===
TELEGRAM_TOKEN = '7970022703:AAEFU0v_402lujK3-FHkP6xW0NXKeteco3U'
TELEGRAM_CHAT_ID = '-1001875640464'
USERNAME = 'elonmusk'  # Thay tên khác nếu muốn
CHECK_INTERVAL = 60  # giây

last_tweet_id = None

def send_telegram_message(text):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': text}
    r = requests.post(url, data=data)
    if r.status_code != 200:
        print(f'⚠️ Telegram error: {r.text}')

def get_latest_tweet():
    try:
        scraper = sntwitter.TwitterUserScraper(USERNAME)
        tweet = next(scraper.get_items())
        return tweet
    except Exception as e:
        print(f'⚠️ Lỗi khi scrape tweet: {e}')
        return None

def main():
    global last_tweet_id
    print(f"👁️ Đang theo dõi @{USERNAME} không cần API chính chủ")

    while True:
        tweet = get_latest_tweet()
        if tweet and tweet.id != last_tweet_id:
            msg = f"🧵 Tweet mới từ @{USERNAME}:\n\n{tweet.content}\n\nhttps://x.com/{USERNAME}/status/{tweet.id}"
            send_telegram_message(msg)
            last_tweet_id = tweet.id
            print(f"✅ Đã gửi tweet: {tweet.id}")
        else:
            print("⌛ Không có tweet mới.")
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
