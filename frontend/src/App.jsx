import { useState } from "react";
import NewsFetcher from "./components/NewsFetcher.jsx";
import AnalysisPanel from "./components/AnalysisPanel.jsx";
import ChartPanel from "./components/ChartPanel.jsx";

export default function App() {
  const [newsItems, setNewsItems] = useState([]);
  const [analysisText, setAnalysisText] = useState("");
  const [chartData, setChartData] = useState("");

  const handleNewsFetched = (items) => {
    setNewsItems(items);

    const combinedText = items
      .map((item) => `${item.title || ""}\n${item.content || ""}`.trim())
      .filter(Boolean)
      .join("\n");
    setAnalysisText(combinedText || "Great product\nBad experience");

    const sourceCounts = items.reduce((acc, item) => {
      const key = item.source || "Unknown";
      acc[key] = (acc[key] || 0) + 1;
      return acc;
    }, {});
    const sourceData = Object.entries(sourceCounts).map(([label, value]) => ({
      label,
      value,
    }));
    if (sourceData.length) {
      setChartData(JSON.stringify(sourceData, null, 2));
    }
  };

  const handleAnalysisResults = ({ method, results }) => {
    if (method === "sentiment") {
      const sentimentCounts = results.reduce((acc, item) => {
        const key = item.sentiment || "unknown";
        acc[key] = (acc[key] || 0) + 1;
        return acc;
      }, {});
      const sentimentData = Object.entries(sentimentCounts).map(([label, value]) => ({
        label,
        value,
      }));
      if (sentimentData.length) {
        setChartData(JSON.stringify(sentimentData, null, 2));
      }
    }

    if (method === "topic" && results.document_topics) {
      const topicCounts = results.document_topics.reduce((acc, item) => {
        const key = `Topic ${item.topic_id}`;
        acc[key] = (acc[key] || 0) + 1;
        return acc;
      }, {});
      const topicData = Object.entries(topicCounts).map(([label, value]) => ({
        label,
        value,
      }));
      if (topicData.length) {
        setChartData(JSON.stringify(topicData, null, 2));
      }
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>DataSciProject</h1>
        <p>News fetching, analysis, and visualization</p>
      </header>

      <main className="grid">
        <section className="card">
          <h2>News Fetch</h2>
          <NewsFetcher onFetched={handleNewsFetched} />
        </section>

        <section className="card">
          <h2>Text Analysis</h2>
          <AnalysisPanel initialTexts={analysisText} onResults={handleAnalysisResults} />
        </section>

        <section className="card">
          <h2>Visualization</h2>
          <ChartPanel inputData={chartData} />
        </section>
      </main>
    </div>
  );
}
