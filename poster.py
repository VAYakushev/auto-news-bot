import telebot
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID, PROXY
import logging
import time
import requests
import re
from io import BytesIO
import html

logging.basicConfig(level=logging.INFO, encoding='utf-8')
logger = logging.getLogger(__name__)

if PROXY:
    import telebot.apihelper
    telebot.apihelper.PROXY = PROXY

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


def download_image(url: str) -> bytes | None:
    urls_to_try = []
    
    if not url or len(url) < 10:
        return None
    
    url_clean = re.sub(r'/\d+_\d+x\d+', '', url)
    url_clean = re.sub(r'[?&].*$', '', url_clean)
    
    if "_top_pics" in url_clean:
        urls_to_try.append(url_clean.replace("/top_pics/", "/top_pics/media/"))
        urls_to_try.append(url_clean.replace("/top_pics/", "/top_pics/resize/"))
    
    if ".drom.ru" in url_clean:
        base = url_clean.replace(".drom.ru", "")
        if "/i" not in base:
            parts = base.split("/")
            for i, p in enumerate(parts):
                if p.isdigit():
                    parts[i] = f"i{p}"
                    urls_to_try.append("/".join(parts) + "/gen340_full.jpg")
                    break
    
    urls_to_try.append(url_clean)
    urls_to_try.append(url)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }
    
    for img_url in urls_to_try:
        try:
            resp = requests.get(img_url, timeout=15, headers=headers)
            if resp.status_code == 200 and 5000 < len(resp.content) < 5000000:
                return resp.content
        except Exception:
            pass
    
    return None


def highlight_key_facts(description: str) -> str:
    positive_keywords = [
        "премьера", "впервые", "новый", "запуск", "дебют", "представлен",
        "электро", "гибрид", "автономный", "рекорд", "победил", "уникальный",
        "мощность", "запас хода", "быстрая зарядка", "безопасность"
    ]
    
    sentences = description.split(".")
    highlighted = []
    for sent in sentences[:10]:
        sent = sent.strip()
        if not sent:
            continue
        if not sent.endswith("."):
            sent += "."
        for kw in positive_keywords:
            if kw.lower() in sent.lower():
                highlighted.append(f"✅ {sent}")
                break
        else:
            if len(highlighted) < 3:
                highlighted.append(sent)
    
    return "\n".join(highlighted) if highlighted else description[:600]


def format_single_news(news_item: dict) -> str:
    title = html.unescape(news_item.get("title", "Без названия"))
    description = html.unescape(news_item.get("description", ""))
    source = html.unescape(news_item.get("source", ""))
    url = news_item.get("url", "")
    
    text = highlight_key_facts(description)
    
    msg = f"🚗 *{title}*\n\n"
    msg += f"{text}\n\n"
    msg += f"📍 {source} | [Подробнее]({url})"
    
    return msg


def post_single_news(news_item: dict) -> bool:
    try:
        image_url = news_item.get("image", "")
        message = format_single_news(news_item)
        
        if image_url and len(image_url) > 10:
            img_data = download_image(image_url)
            if img_data:
                bot.send_photo(TELEGRAM_CHANNEL_ID, img_data, caption=message, parse_mode="Markdown")
                logger.info(f"Posted with image: {news_item.get('title', '')[:50]}")
                time.sleep(3)
                return True
        
        bot.send_message(TELEGRAM_CHANNEL_ID, message, parse_mode="Markdown")
        logger.info(f"Posted text: {news_item.get('title', '')[:50]}")
        time.sleep(3)
        return True
    
    except Exception as e:
        logger.error(f"Error posting: {e}")
        return False


def post_news_batch(news_list: list) -> int:
    posted = 0
    for news_item in news_list:
        if post_single_news(news_item):
            posted += 1
    return posted