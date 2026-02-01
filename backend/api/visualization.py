"""
Visualization API Routes
Handles chart generation endpoints
"""
from flask import Blueprint, request, jsonify
import logging

from backend.visualization.chart_generator import ChartGenerator

logger = logging.getLogger(__name__)
viz_bp = Blueprint('visualization', __name__, url_prefix='/api/viz')

@viz_bp.route('/generate', methods=['POST'])
def generate_chart():
    """
    Generate a chart configuration for frontend rendering
    Accepts JSON: {
        'data': [{'label': str, 'value': num}, ...],
        'chart_type': 'bar'|'line'|'pie'|'scatter',
        'title': str (optional),
        'x_label': str (optional),
        'y_label': str (optional)
    }
    """
    data = request.get_json()
    if not data or 'data' not in data:
        return jsonify({'error': 'Please provide chart data'}), 400
    
    chart_data = data.get('data', [])
    chart_type = data.get('chart_type', 'bar')
    title = data.get('title', 'Data Visualization')
    x_label = data.get('x_label', 'Category')
    y_label = data.get('y_label', 'Value')
    
    if not chart_data:
        return jsonify({'error': 'Chart data cannot be empty'}), 400
    
    try:
        generator = ChartGenerator()
        plot_config = generator.generate(
            data=chart_data,
            chart_type=chart_type,
            title=title,
            x_label=x_label,
            y_label=y_label
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

@viz_bp.route('/types', methods=['GET'])
def get_chart_types():
    """
    Get supported chart types
    """
    return jsonify({
        'status': 'success',
        'types': [
            {'id': 'bar', 'name': 'Bar Chart'},
            {'id': 'line', 'name': 'Line Chart'},
            {'id': 'pie', 'name': 'Pie Chart'},
            {'id': 'scatter', 'name': 'Scatter Plot'},
            {'id': 'heatmap', 'name': 'Heatmap'}
        ]
    })
