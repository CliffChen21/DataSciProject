import { useState } from "react";
import { api } from "../services/api.js";

export default function NewsFetcher({ onFetched }) {
  const [keyword, setKeyword] = useState("AI");
  const [limit, setLimit] = useState(5);
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchNews = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await api.get("/api/news/fetch", {
        params: { keyword, limit },
      });
      const data = response.data.data || [];
      setItems(data);
      if (onFetched) {
        onFetched(data);
      }
    } catch (err) {
      setError(err?.response?.data?.error || "Failed to fetch news");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="row">
        <input
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          placeholder="Keyword"
        />
        <input
          type="number"
          value={limit}
          min={1}
          max={20}
          onChange={(e) => setLimit(Number(e.target.value))}
        />
        <button onClick={fetchNews} disabled={loading}>
          {loading ? "Loading..." : "Fetch"}
        </button>
      </div>

      {error && <p className="error">{error}</p>}

      <ul className="list">
        {items.map((item) => (
          <li key={item.id || item.url}>
            <strong>{item.title}</strong>
            <div className="meta">{item.source}</div>
            <p>{item.content}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
