import requests
import time

# === Config ===
TELEGRAM_TOKEN = '7970022703:AAEFU0v_402lujK3-FHkP6xW0NXKeteco3U'
TELEGRAM_CHAT_ID = '-1001875640464'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAA5n2gEAAAAAibiT0Bkqvv7ujTpfPTfk91j4JJc%3Dr6C6PF40UM8lUWcW8a7bCEovvNhYErMIIM547uQ95Z0dR5iMwh'
USERNAME = 'JnP6900erc'
USER_ID = '1644057593241622529'

last_tweet_id = None

def send_telegram_message(text):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': text}
    try:
        r = requests.post(url, data=data)
        if r.status_code != 200:
            print(f'⚠️ Telegram lỗi: {r.text}')
    except Exception as e:
        print(f'⚠️ Lỗi gửi Telegram: {e}')

def get_latest_tweet():
    url = f'https://api.twitter.com/2/users/{USER_ID}/tweets?max_results=5&tweet.fields=created_at'
    headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        tweets = r.json().get('data', [])
        return tweets[0] if tweets else None
    except Exception as e:
        print(f'⚠️ Lỗi lấy tweet: {e}')
        return None

def main():
    global last_tweet_id
    print(f"👀 Đang theo dõi: {USERNAME}")

    while True:
        tweet = get_latest_tweet()
        if tweet:
            tweet_id = tweet['id']
            if last_tweet_id != tweet_id:
                msg = f"🧵 Tweet mới từ @{USERNAME}:\n\n{tweet['text']}\n\nhttps://x.com/{USERNAME}/status/{tweet_id}"
                send_telegram_message(msg)
                last_tweet_id = tweet_id
                print(f"[+] Gửi tweet @{USERNAME}")
        time.sleep(65)

if __name__ == '__main__':
    main()
