"""Unit tests for TextAnalyzer."""
import pytest

from backend.analysis.text_analyzer import TextAnalyzer


@pytest.fixture(autouse=True)
def disable_pipeline(monkeypatch):
    def fake_pipeline(*args, **kwargs):
        raise RuntimeError("model load failed")

    monkeypatch.setattr("backend.analysis.text_analyzer.pipeline", fake_pipeline)


def test_load_models_failure():
    analyzer = TextAnalyzer()
    assert analyzer.sentiment_model is None


def test_analyze_sentiment_fallback():
    analyzer = TextAnalyzer()
    results = analyzer.analyze_sentiment(["short", "longer text"])
    assert len(results) == 2
    assert "sentiment" in results[0]


def test_topic_modeling_basic():
    analyzer = TextAnalyzer()
    texts = ["machine learning is fun", "deep learning with transformers", "ai models"]
    results = analyzer.topic_modeling(texts, num_topics=2)
    assert results["num_topics"] == 2
    assert len(results["topics"]) == 2


def test_keyword_extraction_basic():
    analyzer = TextAnalyzer()
    keywords = analyzer.extract_keywords("simple text for keyword extraction", top_k=3)
    assert len(keywords) == 3
