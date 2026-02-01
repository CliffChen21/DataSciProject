"""Unit tests for text preprocessing and analysis utilities."""
from backend.analysis.text_preprocessor import TextPreprocessor
from backend.analysis.text_analyzer import TextAnalyzer


def test_text_cleaning():
    preprocessor = TextPreprocessor()
    text = "Visit https://example.com now! Email test@example.com"
    cleaned = preprocessor.clean_text(text)
    assert "http" not in cleaned
    assert "@" not in cleaned


def test_text_tokenize_english():
    preprocessor = TextPreprocessor()
    tokens = preprocessor.tokenize("Hello world", language="english")
    assert tokens == ["hello", "world"]


def test_text_tokenize_chinese_fallback():
    preprocessor = TextPreprocessor()
    tokens = preprocessor.tokenize("中文测试", language="chinese")
    assert len(tokens) > 0


def test_keyword_extraction_fallback():
    analyzer = TextAnalyzer()
    keywords = analyzer.extract_keywords("simple text for keyword extraction", top_k=3)
    assert len(keywords) == 3
