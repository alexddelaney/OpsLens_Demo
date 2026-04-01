import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

function App() {
  const [metrics, setMetrics] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/metrics/ws");

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMetrics(data);
      setLoading(false);
    };

    ws.onerror = () => console.error("WebSocket error");

    const alertInterval = setInterval(() => {
      fetch("http://127.0.0.1:8000/metrics/alerts")
        .then(res => res.json())
        .then(data => setAlerts(data.alerts || []))
        .catch(err => console.error("Alerts fetch failed:", err));
    }, 5000);

    return () => {
      ws.close();
      clearInterval(alertInterval);
    };
  }, []);

  const merged = {};
  metrics.slice(0, 60).forEach((m) => {
    const time = new Date(m.created_at).toLocaleTimeString();
    if (!merged[time]) merged[time] = { time };
    if (m.name === "cpu_usage") merged[time].cpu = m.value;
    if (m.name === "memory_usage") merged[time].memory = m.value;
  });
  const chartData = Object.values(merged).slice(-30).reverse();

  return (
    <div
      style={{
        padding: "2rem",
        fontFamily: "Arial",
        background: "#0f172a",
        color: "#e5e7eb",
        minHeight: "100vh",
      }}
    >
      <h1 style={{ color: "#38bdf8" }}>OpsLens Dashboard</h1>

      <p style={{ color: "#22c55e", marginBottom: "1rem" }}>
        ● System monitoring active
      </p>

      {loading && (
        <p style={{ color: "#94a3b8" }}>Updating metrics…</p>
      )}

      <h2>System Metrics (Live)</h2>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="cpu" stroke="#ff7300" connectNulls />
          <Line type="monotone" dataKey="memory" stroke="#387908" connectNulls />
        </LineChart>
      </ResponsiveContainer>

      <h2 style={{ marginTop: "2rem" }}>Alerts</h2>

      {alerts.length === 0 ? (
        <p>No anomalies detected</p>
      ) : (
        <ul>
          {alerts.map((a, i) => (
            <li
              key={i}
              style={{
                color: a.severity === "critical" ? "#ef4444" : "#f59e0b",
                marginBottom: "0.25rem",
              }}
            >
              🚨 {a.metric}: {Number(a.value).toFixed(2)} ({a.severity})
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;