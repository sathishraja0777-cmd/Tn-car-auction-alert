import os
import requests
from bs4 import BeautifulSoup

URL = "https://www.eauctionsindia.com/cars"
LOCATIONS = ["chennai", "tiruvallur", "kanchipuram"]

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")


def send_alert(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("Missing Telegram credentials")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message,
        "disable_web_page_preview": True
    })


def main():
    r = requests.get(URL, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")

    links = soup.find_all("a", href=True)

    for link in links:
        text = link.get_text(strip=True).lower()
        href = link["href"]

        if any(loc in text for loc in LOCATIONS):
            msg = (
                "🚗 New Car Auction (Tamil Nadu)\n\n"
                f"📍 Match: {text}\n"
                f"🔗 {href}"
            )
            send_alert(msg)


if __name__ == "__main__":
    main()
