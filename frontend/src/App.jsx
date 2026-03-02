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

  // -------------------------
  // Fetch metrics
  // -------------------------
  const fetchMetrics = async () => {
    try {
      setLoading(true);
      const res = await fetch("http://127.0.0.1:8000/metrics");
      const data = await res.json();
      setMetrics(data);
    } catch (err) {
      console.error("Metrics fetch failed:", err);
    } finally {
      setLoading(false);
    }
  };

  // -------------------------
  // Fetch alerts
  // -------------------------
  const fetchAlerts = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/metrics/alerts");
      const data = await res.json();
      setAlerts(data.alerts || []);
    } catch (err) {
      console.error("Alerts fetch failed:", err);
    }
  };

  // -------------------------
  // Auto refresh
  // -------------------------
  useEffect(() => {
    fetchMetrics();
    fetchAlerts();

    const interval = setInterval(() => {
      fetchMetrics();
      fetchAlerts();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  // -------------------------
  // Prepare chart data
  // -------------------------
  const chartData = metrics
    .slice(0, 30)
    .reverse()
    .map((m) => ({
      time: new Date(m.created_at).toLocaleTimeString(),
      cpu: m.name === "cpu_usage" ? m.value : null,
      memory: m.name === "memory_usage" ? m.value : null,
    }));

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

      {/* ✅ Loading indicator */}
      {loading && (
        <p style={{ color: "#94a3b8" }}>Updating metrics…</p>
      )}

      {/* ============================= */}
      {/* 📊 System Metrics Chart */}
      {/* ============================= */}
      <h2>System Metrics (Live)</h2>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />

          <Line
            type="monotone"
            dataKey="cpu"
            stroke="#ff7300"
            connectNulls
          />
          <Line
            type="monotone"
            dataKey="memory"
            stroke="#387908"
            connectNulls
          />
        </LineChart>
      </ResponsiveContainer>

      {/* ============================= */}
      {/* 🚨 Alerts */}
      {/* ============================= */}
      <h2 style={{ marginTop: "2rem" }}>Alerts</h2>

      {alerts.length === 0 ? (
        <p>No anomalies detected</p>
      ) : (
        <ul>
          {alerts.map((a, i) => (
            <li
              key={i}
              style={{
                color:
                  a.severity === "critical"
                    ? "#ef4444"
                    : "#f59e0b",
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