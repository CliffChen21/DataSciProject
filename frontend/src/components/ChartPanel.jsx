import { useEffect, useState } from "react";
import Plot from "react-plotly.js";
import { api } from "../services/api.js";

export default function ChartPanel({ inputData }) {
  const [chartType, setChartType] = useState("bar");
  const [config, setConfig] = useState(null);
  const [data, setData] = useState(
    JSON.stringify(
      [
        { label: "A", value: 10 },
        { label: "B", value: 20 },
      ],
      null,
      2
    )
  );
  const [error, setError] = useState("");

  useEffect(() => {
    if (inputData) {
      setData(inputData);
    }
  }, [inputData]);

  const generate = async () => {
    setError("");
    try {
      const parsed = JSON.parse(data);
      const response = await api.post("/api/viz/generate", {
        data: parsed,
        chart_type: chartType,
      });
      setConfig(response.data.plot_config);
    } catch (err) {
      setError(err?.response?.data?.error || "Failed to generate chart");
    }
  };

  return (
    <div>
      <div className="row">
        <select value={chartType} onChange={(e) => setChartType(e.target.value)}>
          <option value="bar">Bar</option>
          <option value="line">Line</option>
          <option value="pie">Pie</option>
          <option value="scatter">Scatter</option>
          <option value="heatmap">Heatmap</option>
        </select>
        <button onClick={generate}>Generate</button>
      </div>

      <textarea
        rows={6}
        value={data}
        onChange={(e) => setData(e.target.value)}
        placeholder="Chart data JSON"
      />

      {error && <p className="error">{error}</p>}

      {config && (
        <Plot data={config.data} layout={config.layout} className="plot" />
      )}
    </div>
  );
}
