"""
Web Scraper Module
Handles web scraping for news websites
"""
import logging
from typing import List, Dict
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class WebScraper:
    """
    Web scraper for news websites
    Use as fallback when APIs are not available
    """
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
    
    def scrape_url(self, url: str) -> Dict:
        """
        Scrape a single news article from URL
        
        Args:
            url: Article URL
            
        Returns:
            Dictionary containing article data
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            article_data = {
                'url': url,
                'title': self._extract_title(soup),
                'content': self._extract_content(soup),
                'publish_time': self._extract_publish_time(soup)
            }
            
            logger.info(f'Successfully scraped: {url}')
            return article_data
            
        except Exception as e:
            logger.error(f'Failed to scrape {url}: {str(e)}')
            raise
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract article title from HTML"""
        # Try common title selectors
        title_tag = soup.find('h1') or soup.find('title')
        return title_tag.get_text(strip=True) if title_tag else 'No title'
    
    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract article content from HTML"""
        # Try common content selectors
        content_tags = soup.find_all('p')
        content = ' '.join([p.get_text(strip=True) for p in content_tags[:5]])
        return content if content else 'No content'
    
    def _extract_publish_time(self, soup: BeautifulSoup) -> str:
        """Extract publish time from HTML"""
        # Try common time selectors
        time_tag = soup.find('time')
        if time_tag and time_tag.get('datetime'):
            return time_tag['datetime']
        return 'Unknown'
    
    def scrape_baidu_news(self, keyword: str, limit: int = 10) -> List[Dict]:
        """
        Scrape Baidu News search results
        
        Args:
            keyword: Search keyword
            limit: Maximum number of results
            
        Returns:
            List of news articles from Baidu
            
        Note:
            Baidu may implement anti-scraping measures.
            Consider using Selenium for JavaScript-rendered content.
        """
        try:
            url = f'https://www.baidu.com/s?tn=news&word={keyword}'
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'  # Handle Chinese encoding
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            articles = []
            news_items = soup.select('.result, .result-op, .c-container')[:limit]
            
            for idx, item in enumerate(news_items):
                try:
                    title_tag = item.select_one('h3 a') or item.select_one('a')
                    snippet_tag = (
                        item.select_one('.c-abstract')
                        or item.select_one('.c-span-last')
                        or item.select_one('.content-right_8Zs40')
                    )
                    
                    articles.append({
                        'id': f'baidu_{idx+1}',
                        'title': title_tag.get_text(strip=True) if title_tag else 'No title',
                        'content': snippet_tag.get_text(strip=True) if snippet_tag else 'No content',
                        'url': title_tag.get('href', '') if title_tag else '',
                        'source': 'Baidu News',
                        'language': 'zh-CN'
                    })
                except Exception as e:
                    logger.warning(f'Failed to parse Baidu news item: {e}')
                    continue
            
            logger.info(f'Scraped {len(articles)} articles from Baidu News')
            return articles
            
        except Exception as e:
            logger.error(f'Failed to scrape Baidu News: {str(e)}')
            raise
    
    def scrape_snowball(self, keyword: str, limit: int = 10) -> List[Dict]:
        """
        Scrape Snowball (Xueqiu) financial discussions
        
        Args:
            keyword: Search keyword or stock symbol
            limit: Maximum number of results
            
        Returns:
            List of posts from Snowball
            
        Note:
            Snowball may require authentication for full access.
            Consider using their API if available.
        """
        try:
            # Snowball search endpoint (may require authentication)
            url = f'https://xueqiu.com/statuses/search.json?q={keyword}&count={limit}'
            
            # Add cookies/session if needed for authentication
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # If JSON API is available
            if response.headers.get('content-type', '').startswith('application/json'):
                data = response.json()
                articles = []
                
                for idx, item in enumerate(data.get('list', [])[:limit]):
                    articles.append({
                        'id': f'snowball_{item.get("id", idx)}',
                        'title': item.get('title') or item.get('text', 'No title'),
                        'content': item.get('text', 'No content'),
                        'url': item.get('target', '') or f'https://xueqiu.com/{item.get("id", "")}',
                        'source': 'Snowball (Xueqiu)',
                        'author': (item.get('user', {}) or {}).get('screen_name', item.get('user_name', 'Unknown')),
                        'likes': item.get('like_count', 0),
                        'comments': item.get('reply_count', 0),
                        'language': 'zh-CN'
                    })
                
                logger.info(f'Scraped {len(articles)} posts from Snowball')
                return articles
            else:
                # Fallback to HTML scraping if API not available
                raise NotImplementedError('Snowball HTML scraping not yet implemented')
                
        except Exception as e:
            logger.error(f'Failed to scrape Snowball: {str(e)}')
            raise
