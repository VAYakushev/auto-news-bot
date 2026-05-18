from db import is_already_published
from typing import List, Dict


def filter_new_news(news: List[Dict]) -> List[Dict]:
    filtered = []
    for item in news:
        url = item.get("url", "")
        title = item.get("title", "")
        
        if not url:
            continue
        
        if is_already_published(url, title):
            continue
            
        filtered.append(item)
    
    return filtered


def deduplicate(news: List[Dict]) -> List[Dict]:
    seen_urls = set()
    seen_titles = set()
    unique = []
    for item in news:
        url = item.get("url", "")
        title = item.get("title", "").lower().strip()[:80]
        
        if url and url not in seen_urls:
            seen_urls.add(url)
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique.append(item)
    
    return unique