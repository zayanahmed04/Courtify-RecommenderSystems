import Link from "next/link";

const stats = [
  { value: "100",  label: "Courts in Karachi" },
  { value: "97%",  label: "Model Accuracy" },
  { value: "5ms",  label: "Search Latency" },
  { value: "5",    label: "Sports Covered" },
];

const sports = ["Cricket", "Football", "Padel", "Badminton", "Basketball"];

export default function Home() {
  return (
    <div style={{ maxWidth: 720, margin: "0 auto" }}>

      {/* Header */}
      <div style={{ marginBottom: 40 }}>
        <div style={{
          display: "inline-block",
          fontSize: 11, fontWeight: 600,
          color: "#0F6E56",
          background: "#e8f5ef",
          border: "1px solid #c2dfd4",
          borderRadius: 20, padding: "3px 12px",
          marginBottom: 16, letterSpacing: "0.3px",
          textTransform: "uppercase",
        }}>
          FAST-NUCES Karachi — AI Project
        </div>
        <h1 style={{ fontSize: 36, fontWeight: 700, color: "#111", marginBottom: 12, lineHeight: 1.15, letterSpacing: "-0.5px" }}>
          CourtFind
        </h1>
        <p style={{ fontSize: 16, color: "#555", lineHeight: 1.7, maxWidth: 540 }}>
          Find sports courts near you using A* search, or get matched with the right players using a trained classifier.
        </p>
      </div>

      {/* CTA Buttons */}
      <div style={{ display: "flex", gap: 12, marginBottom: 48 }}>
        <Link href="/courts" style={{
          display: "inline-block",
          padding: "11px 24px",
          background: "#0F6E56", color: "#fff",
          borderRadius: 9, fontSize: 14, fontWeight: 600,
          textDecoration: "none",
          transition: "background 0.12s",
        }}>
          Find a Court
        </Link>
        <Link href="/matchmaking" style={{
          display: "inline-block",
          padding: "11px 24px",
          background: "#fff", color: "#0F6E56",
          border: "1px solid #c2dfd4",
          borderRadius: 9, fontSize: 14, fontWeight: 600,
          textDecoration: "none",
        }}>
          Match Players
        </Link>
      </div>

      {/* Stats */}
      <div style={{
        display: "grid", gridTemplateColumns: "repeat(4, 1fr)",
        gap: 12, marginBottom: 40,
      }}>
        {stats.map((s) => (
          <div key={s.value} style={{
            background: "#fff", border: "1px solid #e4e9e6",
            borderRadius: 10, padding: "16px",
          }}>
            <div style={{ fontSize: 22, fontWeight: 700, color: "#0F6E56", marginBottom: 2 }}>{s.value}</div>
            <div style={{ fontSize: 12, color: "#777" }}>{s.label}</div>
          </div>
        ))}
      </div>

      {/* Two feature blocks */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14, marginBottom: 40 }}>
        <div style={{ background: "#fff", border: "1px solid #e4e9e6", borderRadius: 12, padding: "22px" }}>
          <div style={{ fontWeight: 600, fontSize: 15, marginBottom: 8, color: "#111" }}>Court Search</div>
          <p style={{ fontSize: 13, color: "#666", lineHeight: 1.65, marginBottom: 16 }}>
            Pick a sport, set a budget, and choose your zone. The A* engine scores all 100 courts by distance, price, and rating — returning the best matches ranked by heuristic score.
          </p>
          <Link href="/courts" style={{ fontSize: 13, fontWeight: 600, color: "#0F6E56", textDecoration: "none" }}>
            Search courts →
          </Link>
        </div>
        <div style={{ background: "#fff", border: "1px solid #e4e9e6", borderRadius: 12, padding: "22px" }}>
          <div style={{ fontWeight: 600, fontSize: 15, marginBottom: 8, color: "#111" }}>Player Matchmaking</div>
          <p style={{ fontSize: 13, color: "#666", lineHeight: 1.65, marginBottom: 16 }}>
            Enter your skill level, play style, and availability. A Random Forest model trained on 1,000 player profiles predicts your match compatibility class and confidence.
          </p>
          <Link href="/matchmaking" style={{ fontSize: 13, fontWeight: 600, color: "#0F6E56", textDecoration: "none" }}>
            Check compatibility →
          </Link>
        </div>
      </div>

      {/* Sports */}
      <div style={{ background: "#fff", border: "1px solid #e4e9e6", borderRadius: 12, padding: "20px 22px" }}>
        <div style={{ fontSize: 12, fontWeight: 600, color: "#777", textTransform: "uppercase", letterSpacing: "0.4px", marginBottom: 12 }}>
          Supported Sports
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          {sports.map((s) => (
            <span key={s} style={{
              fontSize: 13, fontWeight: 500,
              background: "#f0faf5", color: "#0F6E56",
              border: "1px solid #c2dfd4",
              borderRadius: 6, padding: "5px 12px",
            }}>{s}</span>
          ))}
        </div>
      </div>

    </div>
  );
}
