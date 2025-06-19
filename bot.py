import requests
import time

# === Cấu hình ===
TELEGRAM_TOKEN = '7970022703:AAEFU0v_402lujK3-FHkP6xW0NXKeteco3U'
TELEGRAM_CHAT_ID = '-1001875640464'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAA5n2gEAAAAALRZu85jICz2w1EgailHagT3HtIk%3DSb4q6gejim2qIlOrLgKUGdWn1x45lLj2Y2N3VqoliZ6VNUGzt5'

# === Map username → user_id ===
TWITTER_USERS = {
    'JnP6900erc': '1644057593241622529',
    'elonmusk': '44196397',
    'cz_binance': '1150512580',
    'VitalikButerin': '295218901'
}

# === Lưu trạng thái tweet cuối ===
last_tweet_ids = {}

# === Gửi Telegram ===
def send_telegram_message(text):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': text}
    try:
        r = requests.post(url, data=data)
        if r.status_code != 200:
            print(f'⚠️ Telegram lỗi: {r.text}')
    except Exception as e:
        print(f'⚠️ Lỗi gửi Telegram: {e}')

# === Lấy tweet mới nhất của user ===
def get_latest_tweet(user_id):
    url = f'https://api.twitter.com/2/users/{user_id}/tweets?max_results=5&tweet.fields=created_at'
    headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        tweets = r.json().get('data', [])
        return tweets[0] if tweets else None
    except Exception as e:
        print(f'⚠️ Lỗi khi lấy tweet user {user_id}: {e}')
        return None

# === Bot chạy vĩnh viễn ===
def main():
    print(f"👀 Đang theo dõi: {', '.join(TWITTER_USERS.keys())}")

    while True:
        for username, user_id in TWITTER_USERS.items():
            tweet = get_latest_tweet(user_id)
            if tweet:
                tweet_id = tweet['id']
                if last_tweet_ids.get(username) != tweet_id:
                    url = f"https://x.com/{username}/status/{tweet_id}"
                    msg = f"🧵 Tweet mới từ @{username}:\n\n{tweet['text']}\n\n{url}"
                    send_telegram_message(msg)
                    last_tweet_ids[username] = tweet_id
                    print(f"[+] Đã gửi tweet mới của @{username}")
        time.sleep(60)

if __name__ == '__main__':
    main()
