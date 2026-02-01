"""Unit tests for news fetching."""
import types

from backend.data.news_fetcher import NewsFetcher


def test_fetch_rss_news(monkeypatch):
    fetcher = NewsFetcher()

    class DummyFeed:
        def __init__(self):
            self.entries = [
                {"title": "AI breakthrough", "summary": "AI news", "link": "http://x", "id": "1"}
            ]
            self.feed = {"title": "Dummy RSS"}

    def fake_parse(url):
        return DummyFeed()

    monkeypatch.setattr("backend.data.news_fetcher.feedparser.parse", fake_parse)

    results = fetcher._fetch_rss_news("AI", limit=1)
    assert len(results) == 1
    assert results[0]["source"] == "Dummy RSS"


def test_fetch_google_news(monkeypatch):
    fetcher = NewsFetcher()

    monkeypatch.setattr("backend.data.news_fetcher.config.NEWS_API_KEY", "dummy")

    class DummyResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "articles": [
                    {"title": "AI News", "description": "Desc", "source": {"name": "NewsAPI"}, "publishedAt": "2026"}
                ]
            }

    def fake_get(url, params=None, headers=None, timeout=10):
        return DummyResponse()

    monkeypatch.setattr("backend.data.news_fetcher.requests.get", fake_get)

    results = fetcher._fetch_google_news("AI", limit=1)
    assert len(results) == 1
    assert results[0]["source"] == "NewsAPI"


def test_fetch_bing_news(monkeypatch):
    fetcher = NewsFetcher()

    monkeypatch.setattr("backend.data.news_fetcher.config.BING_NEWS_API_KEY", "dummy")

    class DummyResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "value": [
                    {"name": "Bing AI", "description": "Desc", "provider": [{"name": "Bing"}], "datePublished": "2026"}
                ]
            }

    def fake_get(url, params=None, headers=None, timeout=10):
        return DummyResponse()

    monkeypatch.setattr("backend.data.news_fetcher.requests.get", fake_get)

    results = fetcher._fetch_bing_news("AI", limit=1)
    assert len(results) == 1
    assert results[0]["source"] == "Bing"


def test_fetch_fallback_to_mock(monkeypatch):
    fetcher = NewsFetcher()

    # Force all sources to fail or return empty
    fetcher.sources["google_news"] = False
    fetcher.sources["bing_news"] = False
    fetcher.sources["rss"] = False
    fetcher.sources["baidu_news"] = False
    fetcher.sources["snowball"] = False

    results = fetcher.fetch("AI", limit=2)
    assert len(results) == 2
    assert results[0]["id"].startswith("news_")
