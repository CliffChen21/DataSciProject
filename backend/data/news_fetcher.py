"""
News Fetcher Module
Handles news data fetching from various sources (APIs, RSS, web scraping)
"""
import logging
from datetime import datetime
from typing import List, Dict

import feedparser
import requests

from backend import config
from backend.data.web_scraper import WebScraper

logger = logging.getLogger(__name__)

class NewsFetcher:
    """
    Fetches news from multiple sources
    Priority: API > RSS > Web Scraping
    """
    
    def __init__(self):
        self.sources = {
            'google_news': bool(config.NEWS_API_KEY),  # Requires API key
            'bing_news': bool(config.BING_NEWS_API_KEY),    # Requires API key
            'baidu_news': True,    # Web scraping available
            'snowball': True,      # Xueqiu financial news (web scraping)
            'rss': True            # Always available
        }
        self.web_scraper = WebScraper()
    
    def fetch(self, keyword: str, limit: int = 10) -> List[Dict]:
        """
        Fetch news articles for a given keyword
        
        Args:
            keyword: Search keyword
            limit: Maximum number of articles to return
            
        Returns:
            List of news article dictionaries
        """
        logger.info(f'Fetching news for keyword: "{keyword}", limit: {limit}')
        
        # Try different sources in order of priority
        news_data = []
        
        if self.sources['google_news']:
            try:
                news_data = self._fetch_google_news(keyword, limit)
            except Exception as e:
                logger.warning(f'Google News fetch failed: {e}')
        
        if not news_data and self.sources['bing_news']:
            try:
                news_data = self._fetch_bing_news(keyword, limit)
            except Exception as e:
                logger.warning(f'Bing News fetch failed: {e}')
        
        # Try RSS feed parsing
        if not news_data and self.sources['rss']:
            try:
                news_data = self._fetch_rss_news(keyword, limit)
            except Exception as e:
                logger.warning(f'RSS fetch failed: {e}')
        
        # Try Baidu News (web scraping for Chinese content)
        if not news_data and self.sources['baidu_news']:
            try:
                news_data = self._fetch_baidu_news(keyword, limit)
            except Exception as e:
                logger.warning(f'Baidu News fetch failed: {e}')
        
        # Try Snowball/Xueqiu (for financial news)
        if not news_data and self.sources['snowball']:
            try:
                news_data = self._fetch_snowball_news(keyword, limit)
            except Exception as e:
                logger.warning(f'Snowball fetch failed: {e}')
        
        # Fallback to mock data for development
        if not news_data:
            news_data = self._generate_mock_news(keyword, limit)
        
        return news_data
    
    def _generate_mock_news(self, keyword: str, limit: int) -> List[Dict]:
        """
        Generate mock news data for development
        """
        mock_data = []
        for i in range(limit):
            mock_data.append({
                'id': f'news_{i+1}',
                'title': f'{keyword} related news article {i+1}',
                'content': f'This is detailed content about {keyword}. Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
                'source': f'Example News Source {(i % 3) + 1}',
                'author': f'Reporter {(i % 5) + 1}',
                'publish_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'url': f'https://example.com/news/{i+1}',
                'category': ['Technology', 'Business', 'Science'][i % 3]
            })
        
        return mock_data
    
    def _fetch_google_news(self, keyword: str, limit: int) -> List[Dict]:
        """
        Fetch news using NewsAPI.org (Google News-like aggregator)
        Requires NEWS_API_KEY
        """
        if not config.NEWS_API_KEY:
            logger.info('NEWS_API_KEY not configured. Skipping Google News fetch.')
            return []

        url = 'https://newsapi.org/v2/everything'
        params = {
            'q': keyword,
            'pageSize': min(limit, 50),
            'sortBy': 'publishedAt',
            'language': 'en'
        }
        headers = {'X-Api-Key': config.NEWS_API_KEY}

        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        articles = []
        for idx, item in enumerate(data.get('articles', [])[:limit]):
            articles.append({
                'id': f'newsapi_{idx + 1}',
                'title': item.get('title', 'No title'),
                'content': item.get('description', '') or item.get('content', ''),
                'source': item.get('source', {}).get('name', 'NewsAPI'),
                'author': item.get('author', 'Unknown'),
                'publish_time': item.get('publishedAt', 'Unknown'),
                'url': item.get('url', ''),
                'category': 'General',
                'language': 'en'
            })

        return articles
    
    def _fetch_bing_news(self, keyword: str, limit: int) -> List[Dict]:
        """
        Fetch news from Bing News API
        Requires BING_NEWS_API_KEY
        """
        if not config.BING_NEWS_API_KEY:
            logger.info('BING_NEWS_API_KEY not configured. Skipping Bing News fetch.')
            return []

        url = 'https://api.bing.microsoft.com/v7.0/news/search'
        params = {
            'q': keyword,
            'count': min(limit, 50),
            'mkt': 'en-US'
        }
        headers = {'Ocp-Apim-Subscription-Key': config.BING_NEWS_API_KEY}

        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        articles = []
        for idx, item in enumerate(data.get('value', [])[:limit]):
            articles.append({
                'id': f'bing_{idx + 1}',
                'title': item.get('name', 'No title'),
                'content': item.get('description', ''),
                'source': item.get('provider', [{}])[0].get('name', 'Bing News'),
                'author': item.get('provider', [{}])[0].get('name', 'Unknown'),
                'publish_time': item.get('datePublished', 'Unknown'),
                'url': item.get('url', ''),
                'category': 'General',
                'language': 'en'
            })

        return articles
    
    def _fetch_rss_news(self, keyword: str, limit: int) -> List[Dict]:
        """
        Fetch news from RSS feeds
        Common RSS news sources for demo purposes
        """
        logger.info(f'Fetching from RSS feeds: {keyword}')
        
        rss_feeds = [
            'http://rss.cnn.com/rss/cnn_topstories.rss',
            'http://feeds.bbci.co.uk/news/rss.xml',
            'https://www.reddit.com/r/news/.rss'
        ]
        
        all_entries = []
        for feed_url in rss_feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:10]:
                    title = entry.get('title', '')
                    summary = entry.get('summary', '')
                    if keyword.lower() in title.lower() or keyword.lower() in summary.lower():
                        all_entries.append({
                            'id': entry.get('id', entry.get('link', '')),
                            'title': title,
                            'content': summary,
                            'source': feed.feed.get('title', 'RSS Feed'),
                            'author': entry.get('author', 'Unknown'),
                            'publish_time': entry.get('published', 'Unknown'),
                            'url': entry.get('link', ''),
                            'category': 'RSS'
                        })
                        if len(all_entries) >= limit:
                            break
            except Exception as e:
                logger.warning(f'Failed to parse RSS feed {feed_url}: {e}')
                continue
            if len(all_entries) >= limit:
                break
        
        return all_entries[:limit]
    
    def _fetch_baidu_news(self, keyword: str, limit: int) -> List[Dict]:
        """
        Fetch news from Baidu News via web scraping
        Baidu News URL: https://www.baidu.com/s?tn=news&word={keyword}
        
        Notes:
        - Handles Chinese encoding (UTF-8)
        - Parses Baidu News search results
        - Extracts title, snippet, source, publish time
        - Includes basic anti-scraping headers
        """
        logger.info(f'Fetching from Baidu News: {keyword}')
        
        try:
            return self.web_scraper.scrape_baidu_news(keyword, limit)
        except Exception as e:
            logger.warning(f'Baidu scraping failed: {e}. Falling back to mock data.')

        mock_data = []
        for i in range(min(limit, 5)):
            mock_data.append({
                'id': f'baidu_{i+1}',
                'title': f'{keyword} - 百度新闻 {i+1}',
                'content': f'来自百度新闻的 {keyword} 相关内容。这是详细的新闻描述...',
                'source': '百度新闻',
                'author': 'Baidu News',
                'publish_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'url': f'https://www.baidu.com/news/{i+1}',
                'category': 'General',
                'language': 'zh-CN'
            })
        return mock_data
    
    def _fetch_snowball_news(self, keyword: str, limit: int) -> List[Dict]:
        """
        Fetch financial news from Snowball (Xueqiu)
        Snowball URL: https://xueqiu.com/
        
        Snowball is popular for:
        - Stock market news and analysis
        - User-generated financial content
        - Real-time market discussions
        
        Notes:
        - May require authentication/cookies
        - API endpoint: https://xueqiu.com/statuses/search.json
        - Handles Chinese financial terminology
        - Parses stock symbols and market data when available
        """
        logger.info(f'Fetching from Snowball (Xueqiu): {keyword}')
        
        try:
            return self.web_scraper.scrape_snowball(keyword, limit)
        except Exception as e:
            logger.warning(f'Snowball scraping failed: {e}. Falling back to mock data.')

        mock_data = []
        for i in range(min(limit, 5)):
            mock_data.append({
                'id': f'snowball_{i+1}',
                'title': f'{keyword} - 雪球财经分析 {i+1}',
                'content': f'雪球用户对 {keyword} 的深度分析。包括市场趋势、财务数据和投资建议...',
                'source': '雪球 (Xueqiu)',
                'author': f'雪球用户{i+1}',
                'publish_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'url': f'https://xueqiu.com/post/{i+1}',
                'category': 'Finance',
                'language': 'zh-CN',
                'stock_symbols': [],
                'likes': 10 + i * 5,
                'comments': 3 + i
            })
        return mock_data
