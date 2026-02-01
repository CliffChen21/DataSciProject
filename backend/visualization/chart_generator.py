"""
Chart Generator Module
Generates chart configurations for frontend visualization
"""
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ChartGenerator:
    """
    Generate Plotly chart configurations
    Frontend will render these using react-plotly.js
    """
    
    def __init__(self):
        self.supported_types = ['bar', 'line', 'pie', 'scatter', 'heatmap']
    
    def generate(self, data: List[Dict], chart_type: str = 'bar',
                 title: str = 'Data Visualization',
                 x_label: str = 'Category',
                 y_label: str = 'Value') -> Dict[str, Any]:
        """
        Generate a Plotly chart configuration
        
        Args:
            data: List of dictionaries with 'label' and 'value' keys
            chart_type: Type of chart to generate
            title: Chart title
            x_label: X-axis label
            y_label: Y-axis label
            
        Returns:
            Plotly chart configuration dictionary
        """
        logger.info(f'Generating {chart_type} chart with {len(data)} data points')
        
        if chart_type not in self.supported_types:
            raise ValueError(f'Unsupported chart type: {chart_type}. Supported: {self.supported_types}')
        
        # Extract labels and values
        labels = [item.get('label', f'Item {i}') for i, item in enumerate(data)]
        values = [item.get('value', 0) for item in data]
        
        # Generate chart based on type
        if chart_type == 'bar':
            return self._generate_bar(labels, values, title, x_label, y_label)
        elif chart_type == 'line':
            return self._generate_line(labels, values, title, x_label, y_label)
        elif chart_type == 'pie':
            return self._generate_pie(labels, values, title)
        elif chart_type == 'scatter':
            return self._generate_scatter(labels, values, title, x_label, y_label)
        elif chart_type == 'heatmap':
            return self._generate_heatmap(data, title)
        
        return {}
    
    def _generate_bar(self, labels: List[str], values: List[float],
                      title: str, x_label: str, y_label: str) -> Dict:
        """Generate bar chart configuration"""
        return {
            'data': [{
                'x': labels,
                'y': values,
                'type': 'bar',
                'marker': {'color': 'rgb(55, 128, 191)'}
            }],
            'layout': {
                'title': title,
                'xaxis': {'title': x_label},
                'yaxis': {'title': y_label},
                'showlegend': False
            }
        }
    
    def _generate_line(self, labels: List[str], values: List[float],
                       title: str, x_label: str, y_label: str) -> Dict:
        """Generate line chart configuration"""
        return {
            'data': [{
                'x': labels,
                'y': values,
                'type': 'scatter',
                'mode': 'lines+markers',
                'line': {'color': 'rgb(75, 192, 192)'}
            }],
            'layout': {
                'title': title,
                'xaxis': {'title': x_label},
                'yaxis': {'title': y_label},
                'showlegend': False
            }
        }
    
    def _generate_pie(self, labels: List[str], values: List[float], title: str) -> Dict:
        """Generate pie chart configuration"""
        return {
            'data': [{
                'labels': labels,
                'values': values,
                'type': 'pie',
                'hole': 0.3  # Donut chart
            }],
            'layout': {
                'title': title
            }
        }
    
    def _generate_scatter(self, labels: List[str], values: List[float],
                          title: str, x_label: str, y_label: str) -> Dict:
        """Generate scatter plot configuration"""
        return {
            'data': [{
                'x': list(range(len(labels))),
                'y': values,
                'type': 'scatter',
                'mode': 'markers',
                'marker': {'size': 12, 'color': 'rgb(255, 127, 14)'},
                'text': labels,
                'hoverinfo': 'text+y'
            }],
            'layout': {
                'title': title,
                'xaxis': {'title': x_label},
                'yaxis': {'title': y_label},
                'showlegend': False
            }
        }
    
    def _generate_heatmap(self, data: List[Dict], title: str) -> Dict:
        """Generate heatmap configuration"""
        # Transform data into matrix format for heatmap
        # Expects data with 'x', 'y', 'value' keys or single row
        if data and 'x' in data[0] and 'y' in data[0]:
            # Build 2D matrix from x, y, value pairs
            x_labels = sorted(set(d.get('x', '') for d in data))
            y_labels = sorted(set(d.get('y', '') for d in data))
            z_matrix = [[0] * len(x_labels) for _ in range(len(y_labels))]
            
            for d in data:
                x_idx = x_labels.index(d.get('x', ''))
                y_idx = y_labels.index(d.get('y', ''))
                z_matrix[y_idx][x_idx] = d.get('value', 0)
            
            return {
                'data': [{
                    'z': z_matrix,
                    'x': x_labels,
                    'y': y_labels,
                    'type': 'heatmap',
                    'colorscale': 'Viridis'
                }],
                'layout': {
                    'title': title
                }
            }
        else:
            # Simple single-row heatmap
            return {
                'data': [{
                    'z': [[d.get('value', 0) for d in data]],
                    'x': [d.get('label', f'Item {i}') for i, d in enumerate(data)],
                    'type': 'heatmap',
                    'colorscale': 'Viridis'
                }],
                'layout': {
                    'title': title
                }
            }
