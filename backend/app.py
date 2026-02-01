"""
Flask Application Entry Point
Provides RESTful API for news fetching, text analysis, and data visualization
"""
import logging

from flask import Flask, request, jsonify
from flask_cors import CORS

from backend import config
from backend.api.analysis import analysis_bp
from backend.api.news import news_bp
from backend.api.visualization import viz_bp
from backend.analysis.text_analyzer import TextAnalyzer
from backend.data.news_fetcher import NewsFetcher
from backend.visualization.chart_generator import ChartGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend requests

# Register blueprints
app.register_blueprint(news_bp)
app.register_blueprint(analysis_bp)
app.register_blueprint(viz_bp)

# ==================== API Endpoints ====================

@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'DataSciProject API is running',
        'version': '1.0.0'
    })

# Keep legacy endpoints for backward compatibility
# New code should use blueprint routes under /api/*

@app.route('/fetch_news', methods=['GET'])
def fetch_news():
    """
    Fetch news data
    Parameters: keyword - search keyword
    """
    keyword = request.args.get('keyword', '')
    if not keyword:
        return jsonify({'error': 'Please provide a search keyword'}), 400
    
    try:
        fetcher = NewsFetcher()
        news_data = fetcher.fetch(keyword, limit=10)
        
        logger.info(f'Successfully fetched {len(news_data)} news articles about "{keyword}"')
        return jsonify({
            'status': 'success',
            'keyword': keyword,
            'count': len(news_data),
            'data': news_data
        })
    except Exception as e:
        logger.error(f'Failed to fetch news: {str(e)}')
        return jsonify({'error': f'Failed to fetch news: {str(e)}'}), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Text analysis endpoint
    Accepts JSON: {'texts': [...], 'method': 'sentiment'|'topic'}
    """
    data = request.get_json()
    if not data or 'texts' not in data:
        return jsonify({'error': 'Please provide an array of texts to analyze'}), 400
    
    texts = data.get('texts', [])
    method = data.get('method', 'sentiment')
    
    try:
        analyzer = TextAnalyzer()
        if method == 'sentiment':
            results = analyzer.analyze_sentiment(texts)
        elif method == 'topic':
            results = analyzer.topic_modeling(texts).get('document_topics', [])
        elif method == 'keywords':
            results = [
                {'text': text[:50], 'keywords': analyzer.extract_keywords(text)}
                for text in texts
            ]
        else:
            return jsonify({'error': f'Unsupported analysis method: {method}'}), 400
        
        logger.info(f'Completed {method} analysis on {len(texts)} texts')
        return jsonify({
            'status': 'success',
            'method': method,
            'results': results
        })
    except Exception as e:
        logger.error(f'Text analysis failed: {str(e)}')
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/plot', methods=['POST'])
def plot():
    """
    Generate visualization charts
    Accepts JSON: {'data': [...], 'chart_type': 'bar'|'line'|'pie'}
    """
    data = request.get_json()
    if not data or 'data' not in data:
        return jsonify({'error': 'Please provide visualization data'}), 400
    
    chart_data = data.get('data', [])
    chart_type = data.get('chart_type', 'bar')
    
    try:
        generator = ChartGenerator()
        plot_config = generator.generate(
            data=chart_data,
            chart_type=chart_type,
            title=data.get('title', 'Data Visualization'),
            x_label=data.get('x_label', 'Category'),
            y_label=data.get('y_label', 'Value')
        )
        
        logger.info(f'Generated {chart_type} chart with {len(chart_data)} data points')
        return jsonify({
            'status': 'success',
            'chart_type': chart_type,
            'plot_config': plot_config
        })
    except Exception as e:
        logger.error(f'Chart generation failed: {str(e)}')
        return jsonify({'error': f'Chart generation failed: {str(e)}'}), 500

# ==================== Start Application ====================

if __name__ == '__main__':
    logger.info(f'Starting Flask app on {config.API_HOST}:{config.API_PORT}')
    logger.info(f'Debug mode: {config.DEBUG}')
    app.run(
        debug=config.DEBUG,
        host=config.API_HOST,
        port=config.API_PORT
    )
