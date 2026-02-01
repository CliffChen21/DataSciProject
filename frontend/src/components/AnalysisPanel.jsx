import { useEffect, useState } from "react";
import { api } from "../services/api.js";

export default function AnalysisPanel({ initialTexts, onResults }) {
  const [texts, setTexts] = useState("Great product\nBad experience");
  const [method, setMethod] = useState("sentiment");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (initialTexts) {
      setTexts(initialTexts);
    }
  }, [initialTexts]);

  const analyze = async () => {
    setLoading(true);
    setError("");
    const payload = { texts: texts.split("\n").filter(Boolean) };
    try {
      const url = method === "sentiment" ? "/api/analysis/sentiment" : "/api/analysis/topic";
      if (method === "topic") {
        payload.num_topics = 3;
      }
      const response = await api.post(url, payload);
      const output = response.data.results || [];
      setResults(output);
      if (onResults) {
        onResults({ method, results: output });
      }
    } catch (err) {
      setError(err?.response?.data?.error || "Analysis failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="row">
        <select value={method} onChange={(e) => setMethod(e.target.value)}>
          <option value="sentiment">Sentiment</option>
          <option value="topic">Topic Modeling</option>
        </select>
        <button onClick={analyze} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </div>

      <textarea
        rows={5}
        value={texts}
        onChange={(e) => setTexts(e.target.value)}
        placeholder="Enter one text per line"
      />

      {error && <p className="error">{error}</p>}

      <ul className="list">
        {Array.isArray(results) ? (
          results.map((item, idx) => (
            <li key={idx}>
              <pre>{JSON.stringify(item, null, 2)}</pre>
            </li>
          ))
        ) : (
          <li>
            <pre>{JSON.stringify(results, null, 2)}</pre>
          </li>
        )}
      </ul>
    </div>
  );
}
