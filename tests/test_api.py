"""API endpoint tests."""
import pytest

from backend.app import app as flask_app


@pytest.fixture()
def client(monkeypatch):
    """Flask test client with model loading disabled for speed."""
    from backend.analysis import text_analyzer

    monkeypatch.setattr(text_analyzer.TextAnalyzer, "_load_models", lambda self: None)
    flask_app.config.update(TESTING=True)
    with flask_app.test_client() as test_client:
        yield test_client


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "DataSciProject" in data["message"]


def test_news_sources(client):
    response = client.get("/api/news/sources")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert isinstance(data["sources"], list)


def test_news_fetch(client, monkeypatch):
    from backend.api import news as news_api

    def mock_fetch(self, keyword, limit=10):
        return [
            {
                "id": "news_1",
                "title": f"{keyword} related news",
                "content": "mock content",
                "source": "Mock",
                "publish_time": "2026-02-01",
            }
        ]

    monkeypatch.setattr(news_api.NewsFetcher, "fetch", mock_fetch)

    response = client.get("/api/news/fetch?keyword=ai&limit=1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["count"] == 1


def test_sentiment_analysis(client):
    payload = {"texts": ["Great product", "Bad experience"]}
    response = client.post("/api/analysis/sentiment", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["method"] == "sentiment"
    assert len(data["results"]) == 2


def test_topic_modeling(client):
    payload = {"texts": ["AI is great", "AI and ML", "ML models"], "num_topics": 2}
    response = client.post("/api/analysis/topic", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["method"] == "topic_modeling"


def test_chart_generation(client):
    payload = {
        "data": [{"label": "A", "value": 10}, {"label": "B", "value": 20}],
        "chart_type": "bar",
    }
    response = client.post("/api/viz/generate", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["chart_type"] == "bar"


def test_chart_types(client):
    response = client.get("/api/viz/types")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "bar" in [item["id"] for item in data["types"]]


def test_legacy_fetch_news(client):
    response = client.get("/fetch_news?keyword=ai")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["keyword"] == "ai"


def test_legacy_analyze(client, monkeypatch):
    from backend.app import analyze as legacy_analyze
    from backend.analysis import text_analyzer

    def fake_sentiment(self, texts):
        return [{"text": t, "sentiment": "positive", "score": 0.9} for t in texts]

    monkeypatch.setattr(text_analyzer.TextAnalyzer, "analyze_sentiment", fake_sentiment)

    response = client.post("/analyze", json={"texts": ["hello"], "method": "sentiment"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"


def test_legacy_plot(client):
    response = client.post(
        "/plot",
        json={"data": [{"label": "A", "value": 1}], "chart_type": "bar"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
