import os
import requests
from bs4 import BeautifulSoup

URL = "https://www.eauctionsindia.com/search?category=vehicle"

LOCATIONS = ["chennai", "tiruvallur", "kanchipuram"]
VEHICLE_KEYWORDS = ["car", "vehicle", "four", "motor", "jeep", "van", "suv"]

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def send_alert(message):
    api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(api, data={
        "chat_id": CHAT_ID,
        "text": message,
        "disable_web_page_preview": True
    })


def main():
    r = requests.get(URL, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")

    for card in soup.find_all("a", href=True):
        text = card.get_text(strip=True).lower()
        link = card["href"]

        if any(loc in text for loc in LOCATIONS) and any(v in text for v in VEHICLE_KEYWORDS):
            msg = (
                "🚗 New Car Auction (Tamil Nadu)\n\n"
                f"📍 {text}\n"
                f"🔗 {link}"
            )
            send_alert(msg)


if __name__ == "__main__":
    main()
