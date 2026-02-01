"""
Analysis API Routes
Handles text analysis endpoints (sentiment, topic modeling, etc.)
"""
from flask import Blueprint, request, jsonify
import logging

from backend.analysis.text_analyzer import TextAnalyzer

logger = logging.getLogger(__name__)
analysis_bp = Blueprint('analysis', __name__, url_prefix='/api/analysis')

@analysis_bp.route('/sentiment', methods=['POST'])
def sentiment_analysis():
    """
    Perform sentiment analysis on texts
    Accepts JSON: {'texts': [str, ...]}
    """
    data = request.get_json()
    if not data or 'texts' not in data:
        return jsonify({'error': 'Please provide an array of texts to analyze'}), 400
    
    texts = data.get('texts', [])
    if not texts:
        return jsonify({'error': 'Texts array cannot be empty'}), 400
    
    try:
        analyzer = TextAnalyzer()
        results = analyzer.analyze_sentiment(texts)
        
        logger.info(f'Completed sentiment analysis on {len(texts)} texts')
        return jsonify({
            'status': 'success',
            'method': 'sentiment',
            'count': len(results),
            'results': results
        })
    except Exception as e:
        logger.error(f'Sentiment analysis failed: {str(e)}')
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@analysis_bp.route('/topic', methods=['POST'])
def topic_modeling():
    """
    Perform topic modeling on texts
    Accepts JSON: {'texts': [str, ...], 'num_topics': int}
    """
    data = request.get_json()
    if not data or 'texts' not in data:
        return jsonify({'error': 'Please provide an array of texts to analyze'}), 400
    
    texts = data.get('texts', [])
    num_topics = data.get('num_topics', 3)
    
    if not texts:
        return jsonify({'error': 'Texts array cannot be empty'}), 400
    
    try:
        analyzer = TextAnalyzer()
        results = analyzer.topic_modeling(texts, num_topics=num_topics)
        
        logger.info(f'Completed topic modeling on {len(texts)} texts with {num_topics} topics')
        return jsonify({
            'status': 'success',
            'method': 'topic_modeling',
            'num_topics': num_topics,
            'results': results
        })
    except Exception as e:
        logger.error(f'Topic modeling failed: {str(e)}')
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500
