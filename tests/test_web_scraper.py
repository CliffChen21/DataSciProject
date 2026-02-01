"""Unit tests for web scraper utilities."""
from backend.data.web_scraper import WebScraper


def test_scrape_url(monkeypatch):
    scraper = WebScraper()

    class DummyResponse:
        def __init__(self, content):
            self.content = content

        def raise_for_status(self):
            return None

    html = b"<html><h1>Title</h1><p>Paragraph 1</p><p>Paragraph 2</p><time datetime='2026-02-01'></time></html>"

    def fake_get(url, headers=None, timeout=10):
        return DummyResponse(html)

    monkeypatch.setattr("backend.data.web_scraper.requests.get", fake_get)

    data = scraper.scrape_url("http://example.com")
    assert data["title"] == "Title"
    assert "Paragraph" in data["content"]
    assert data["publish_time"] == "2026-02-01"


def test_scrape_baidu_news(monkeypatch):
    scraper = WebScraper()

    class DummyResponse:
        def __init__(self, content):
            self.content = content
            self.headers = {"content-type": "text/html"}
            self.encoding = "utf-8"

        def raise_for_status(self):
            return None

    html = b"""
    <div class='result'>
        <h3><a href='http://news1'>News 1</a></h3>
        <div class='c-abstract'>Summary 1</div>
    </div>
    """

    def fake_get(url, headers=None, timeout=10):
        return DummyResponse(html)

    monkeypatch.setattr("backend.data.web_scraper.requests.get", fake_get)

    results = scraper.scrape_baidu_news("AI", limit=1)
    assert len(results) == 1
    assert results[0]["title"] == "News 1"
    assert results[0]["content"] == "Summary 1"


def test_scrape_snowball_json(monkeypatch):
    scraper = WebScraper()

    class DummyResponse:
        def __init__(self):
            self.headers = {"content-type": "application/json"}

        def raise_for_status(self):
            return None

        def json(self):
            return {
                "list": [
                    {"id": 123, "title": "Post", "text": "Content", "user_name": "User"}
                ]
            }

    def fake_get(url, headers=None, timeout=10):
        return DummyResponse()

    monkeypatch.setattr("backend.data.web_scraper.requests.get", fake_get)

    results = scraper.scrape_snowball("AI", limit=1)
    assert len(results) == 1
    assert results[0]["title"] == "Post"
