import requests
from xml.etree import ElementTree as ET
from telethon import TelegramClient

# RSS Feed Parsing
RSS_FEED_URL = "https://www.cisa.gov/sites/default/files/cve/cve.xml"  # Example CVE RSS Feed

# Filter keywords for specific software/hardware
FILTER_KEYWORDS = ["M365", "Adobe", "Windows", "Cisco"]  # Add more as needed

def fetch_rss_feed():
    response = requests.get(RSS_FEED_URL)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        for item in root.findall(".//item"):
            title = item.find("title").text if item.find("title") is not None else "No Title"
            link = item.find("link").text if item.find("link") is not None else "No Link"
            description = item.find("description").text if item.find("description") is not None else ""
            
            if any(keyword.lower() in title.lower() or keyword.lower() in description.lower() for keyword in FILTER_KEYWORDS):
                print(f"[RSS] {title}\n{link}\n")
    else:
        print("Failed to fetch RSS feed")

# Telegram Parsing (Requires Telegram API credentials)
API_ID = "your_api_id"  # Replace with your API ID
API_HASH = "your_api_hash"  # Replace with your API Hash
TELEGRAM_CHANNEL = "@https://t.me/thehackernews"  # Replace with target channel username

async def fetch_telegram_messages():
    client = TelegramClient("session_name", API_ID, API_HASH)
    await client.start()
    async for message in client.iter_messages(TELEGRAM_CHANNEL, limit=10):  # Fetch latest messages
        if message.text and any(keyword.lower() in message.text.lower() for keyword in FILTER_KEYWORDS):
            print(f"[Telegram] {message.text}\n")
    await client.disconnect()

if __name__ == "__main__":
    print("Fetching RSS feed...")
    fetch_rss_feed()
    
    print("Fetching Telegram messages...")
    import asyncio
    asyncio.run(fetch_telegram_messages())
