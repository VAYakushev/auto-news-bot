import schedule
import time
import logging
from parser import fetch_all_news, enrich_news, score_news
from filter import filter_new_news, deduplicate
from poster import post_news_batch
from db import mark_as_published
from config import POST_TIMES, NEWS_PER_SESSION

logging.basicConfig(level=logging.INFO, encoding='utf-8')
logger = logging.getLogger(__name__)


def job():
    logger.info("Запуск сбора новостей...")
    
    raw_news = fetch_all_news()
    raw_news = deduplicate(raw_news)
    raw_news = filter_new_news(raw_news)
    
    if not raw_news:
        logger.info("Новых новостей не найдено")
        return
    
    logger.info(f"Найдено {len(raw_news)} новостей, загружаю контент...")
    enriched = enrich_news(raw_news, limit=15)
    
    scored = score_news(enriched)
    top_news = scored[:NEWS_PER_SESSION]
    
    if top_news:
        logger.info(f"Публикую {len(top_news)} лучших новостей")
        posted = post_news_batch(top_news)
        logger.info(f"Опубликовано {posted} новостей")
        
        for item in top_news:
            mark_as_published(item["url"], item.get("title", ""), item.get("source", ""))
    else:
        logger.info("Нет подходящих новостей для публикации")


def run_scheduler():
    for time_str in POST_TIMES:
        schedule.every().day.at(time_str).do(job)
    
    logger.info(f"Планировщик настроен на {POST_TIMES}")
    job()
    
    while True:
        schedule.run_pending()
        time.sleep(60)