from db import is_already_published, get_published_urls
from typing import List, Dict


def filter_new_news(news: List[Dict]) -> List[Dict]:
    published = get_published_urls()
    
    filtered = []
    for item in news:
        url = item.get("url", "")
        title = item.get("title", "")
        
        if not url:
            continue
        
        if url in published:
            continue
        
        if is_already_published(url, title):
            continue
            
        filtered.append(item)
    
    return filtered


def deduplicate(news: List[Dict]) -> List[Dict]:
    seen_urls = set()
    unique = []
    for item in news:
        url = item.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique.append(item)
    return unique