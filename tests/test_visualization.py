"""Unit tests for chart generation."""
import pytest

from backend.visualization.chart_generator import ChartGenerator


def test_generate_bar_chart():
    generator = ChartGenerator()
    config = generator.generate(
        data=[{"label": "A", "value": 10}],
        chart_type="bar",
        title="Test",
        x_label="X",
        y_label="Y",
    )
    assert config["data"][0]["type"] == "bar"
    assert config["layout"]["title"] == "Test"


def test_generate_heatmap_matrix():
    generator = ChartGenerator()
    data = [
        {"x": "A", "y": "Row1", "value": 1},
        {"x": "B", "y": "Row1", "value": 2},
        {"x": "A", "y": "Row2", "value": 3},
    ]
    config = generator.generate(data=data, chart_type="heatmap")
    assert config["data"][0]["type"] == "heatmap"
    assert config["data"][0]["x"] == ["A", "B"]
    assert config["data"][0]["y"] == ["Row1", "Row2"]


def test_generate_heatmap_single_row():
    generator = ChartGenerator()
    data = [{"label": "A", "value": 10}, {"label": "B", "value": 20}]
    config = generator.generate(data=data, chart_type="heatmap")
    assert config["data"][0]["type"] == "heatmap"
    assert config["data"][0]["x"] == ["A", "B"]


def test_generate_invalid_chart_type():
    generator = ChartGenerator()
    with pytest.raises(ValueError):
        generator.generate(data=[{"label": "A", "value": 10}], chart_type="invalid")
