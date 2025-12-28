import requests
from bs4 import BeautifulSoup

URL = "https://www.eauctionsindia.com/cars"
LOCATIONS = ["Chennai", "Tiruvallur", "Kanchipuram"]

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_alert(message):
    api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(api, data={
        "chat_id": CHAT_ID,
        "text": message,
        "disable_web_page_preview": True
    })

def main():
    send_alert("✅ Auction monitor is running from GitHub Actions")
    r = requests.get(URL, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    links = soup.find_all("a", href=True)
    for link in links:
        text = link.get_text(strip=True)
        url = link["href"]

        if any(loc.lower() in text.lower() for loc in LOCATIONS):
            msg = (
                "🚗 New Car Auction (Tamil Nadu)\n\n"
                f"📍 Match: {text}\n"
                f"🔗 {url}"
            )
            send_alert(msg)

if __name__ == "__main__":
    main()
