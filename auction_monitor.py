import os
import requests
from bs4 import BeautifulSoup

URL = "https://www.eauctionsindia.com/cars"
LOCATIONS = ["chennai", "tiruvallur", "kanchipuram"]
SEEN_FILE = "seen.txt"

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")


def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message,
        "disable_web_page_preview": True
    })


def load_seen():
    if not os.path.exists(SEEN_FILE):
        return set()
    with open(SEEN_FILE, "r") as f:
        return set(line.strip() for line in f)


def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        for item in seen:
            f.write(item + "\n")


def main():
    seen = load_seen()

    r = requests.get(URL, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")

    for link in soup.find_all("a", href=True):
        text = link.get_text(strip=True).lower()
        href = link["href"]

        if any(loc in text for loc in LOCATIONS):
            if href not in seen:
                msg = (
                    "🚗 New Car Auction (Tamil Nadu)\n\n"
                    f"📍 Match: {text}\n"
                    f"🔗 {href}"
                )
                send_alert(msg)
                seen.add(href)

    save_seen(seen)


if __name__ == "__main__":
    main()
