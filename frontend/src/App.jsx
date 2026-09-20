import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip
} from "recharts";
function App() {
  const [alerts, setAlerts] = useState([]);
  const [analysis, setAnalysis] = useState("");
const totalAlerts = alerts.length;
const openAlerts = alerts.filter(
  (a) => a.status === "Open"
).length;

const resolvedAlerts = alerts.filter(
  (a) => a.status === "Resolved"
).length;

const criticalAlerts = alerts.filter(
  (a) => a.severity === "Critical"
).length;
const API_URL = "https://cyberfusion-a8hb.onrender.com";

const resolveAlert = async (id) => {
  await fetch(`${API_URL}/resolve/${id}`, {
    method: "PUT",
  });

  const res = await fetch(`${API_URL}/alerts`);
  const data = await res.json();

  setAlerts(data);
};

useEffect(() => {
  fetch(`${API_URL}/alerts`)
    .then((res) => res.json())
    .then((data) => setAlerts(data))
    .catch((err) => console.log(err));
}, []);
  const analyzeAlert = async (id) => {
    const res = await fetch(
`https://cyberfusion-a8hb.onrender.com/analyze/${id}`
    );

    const data = await res.json();

    setAnalysis(data.analysis);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>CyberFusion Dashboard</h1>
     <div
  style={{
    display: "flex",
    gap: "20px",
    marginBottom: "20px",
    fontWeight: "bold",
  }}
>
  <div>Total Alerts: {totalAlerts}</div>
  <div>Open Alerts: {openAlerts}</div>
  <div>Resolved Alerts: {resolvedAlerts}</div>
  <div>Critical Alerts: {criticalAlerts}</div>
</div>
      <h2>Security Alerts</h2>
      <p>Total Alerts: {alerts.length}</p>

      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>ID</th>
            <th>Attack Type</th>
            <th>Severity</th>
            <th>Risk Score</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          {alerts.map((alert) => (
            <tr key={alert.id}>
              <td>{alert.id}</td>
              <td>{alert.attack_type}</td>
              <td
  style={{
    color:
      alert.severity === "Critical"
        ? "darkred"
        : alert.severity === "High"
        ? "red"
        : alert.severity === "Medium"
        ? "orange"
        : "green",
    fontWeight: "bold",
  }}
>
  {alert.severity}
</td>
              <td>{alert.risk_score}</td>
<td
  style={{
    color: alert.status === "Open" ? "red" : "green",
    fontWeight: "bold",
  }}
>
  {alert.status}
</td>              <td>
  <td>
  <button onClick={() => resolveAlert(alert.id)}>
    Resolve
  </button>
</td>              <button
                  onClick={() => analyzeAlert(alert.id)}
                >
                  Analyze
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

     <h2>Risk Score Overview</h2>

<BarChart
  width={700}
  height={300}
  data={alerts}
>
  <CartesianGrid strokeDasharray="3 3" />
  <XAxis dataKey="attack_type" />
  <YAxis />
  <Tooltip />
  <Bar dataKey="risk_score" />
</BarChart>
 <h2>AI Analysis</h2>

      <pre
        style={{
          background: "#f0f0f0",
          padding: "10px",
          whiteSpace: "pre-wrap",
        }}
      >
        {analysis}
      </pre>
    </div>
  );
}

export default App;
