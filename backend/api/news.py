"""
News API Routes
Handles news fetching and retrieval endpoints
"""
from flask import Blueprint, request, jsonify
import logging

from backend.data.news_fetcher import NewsFetcher

logger = logging.getLogger(__name__)
news_bp = Blueprint('news', __name__, url_prefix='/api/news')

@news_bp.route('/fetch', methods=['GET'])
def fetch_news():
    """
    Fetch news articles based on keyword
    Query params: keyword (required), limit (optional, default=10)
    """
    keyword = request.args.get('keyword', '')
    limit = int(request.args.get('limit', 10))
    
    if not keyword:
        return jsonify({'error': 'Please provide a search keyword'}), 400
    
    try:
        fetcher = NewsFetcher()
        news_data = fetcher.fetch(keyword, limit=limit)
        
        logger.info(f'Successfully fetched {len(news_data)} news articles for "{keyword}"')
        return jsonify({
            'status': 'success',
            'keyword': keyword,
            'count': len(news_data),
            'data': news_data
        })
    except Exception as e:
        logger.error(f'Failed to fetch news: {str(e)}')
        return jsonify({'error': f'Failed to fetch news: {str(e)}'}), 500

@news_bp.route('/sources', methods=['GET'])
def get_sources():
    """
    Get available news sources
    """
    return jsonify({
        'status': 'success',
        'sources': [
            {'id': 'google_news', 'name': 'Google News', 'enabled': False, 'language': 'en'},
            {'id': 'bing_news', 'name': 'Bing News', 'enabled': False, 'language': 'en'},
            {'id': 'baidu_news', 'name': 'Baidu News (百度新闻)', 'enabled': True, 'language': 'zh-CN'},
            {'id': 'snowball', 'name': 'Snowball/Xueqiu (雪球)', 'enabled': True, 'language': 'zh-CN', 'type': 'financial'},
            {'id': 'rss', 'name': 'RSS Feeds', 'enabled': True, 'language': 'multi'}
        ]
    })
