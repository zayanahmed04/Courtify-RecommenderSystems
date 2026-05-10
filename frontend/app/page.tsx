import Link from "next/link";

const features = [
  {
    icon: "🎯",
    title: "A* Court Search",
    desc: "Finds the best courts using a multi-factor heuristic: distance, price, and rating — scored via priority queue.",
    href: "/courts",
    cta: "Search Courts",
    bg: "#E1F5EE",
    color: "#0F6E56",
  },
  {
    icon: "🤝",
    title: "ML Matchmaking",
    desc: "Random Forest classifier predicts player compatibility (Low / Mid / High) with 97% accuracy using 9 player features.",
    href: "/matchmaking",
    cta: "Find Players",
    bg: "#E6F1FB",
    color: "#185FA5",
  },
  {
    icon: "⚙️",
    title: "How It Works",
    desc: "Explore the A* algorithm, ML pipeline, feature engineering, SMOTE balancing, and the full production architecture.",
    href: "/how-it-works",
    cta: "Learn More",
    bg: "#EEEDFE",
    color: "#534AB7",
  },
];

const stats = [
  { value: "97%", label: "ML Accuracy" },
  { value: "5ms", label: "A* @ 5k Courts" },
  { value: "47", label: "Tests Passing" },
  { value: "3", label: "API Endpoints" },
];

const sports = ["Cricket", "Football", "Padel", "Badminton", "Basketball"];

export default function Home() {
  return (
    <div>
      <div style={{
        background: "linear-gradient(135deg, #085041 0%, #0F6E56 55%, #1D9E75 100%)",
        borderRadius: 18,
        padding: "40px 36px",
        marginBottom: 28,
        position: "relative",
        overflow: "hidden",
      }}>
        <div style={{ position: "relative" }}>
          <div style={{
            display: "inline-flex", alignItems: "center", gap: 6,
            background: "rgba(255,255,255,0.15)",
            border: "1px solid rgba(255,255,255,0.2)",
            borderRadius: 20, padding: "4px 12px",
            fontSize: 12, color: "rgba(255,255,255,0.9)",
            fontWeight: 500, marginBottom: 16,
          }}>
            🏆 AI Project — FAST-NUCES Karachi
          </div>
          <h1 style={{ fontSize: 32, fontWeight: 700, color: "#fff", marginBottom: 10, lineHeight: 1.2 }}>
            CourtFind AI
          </h1>
          <p style={{ fontSize: 16, color: "rgba(255,255,255,0.8)", marginBottom: 24, maxWidth: 480, lineHeight: 1.6 }}>
            Production-grade AI system for intelligent sports court discovery using A* Search and player matchmaking using Machine Learning.
          </p>
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
            {sports.map((s) => (
              <span key={s} style={{
                background: "rgba(255,255,255,0.12)",
                border: "1px solid rgba(255,255,255,0.2)",
                borderRadius: 20, padding: "4px 12px",
                fontSize: 12, color: "rgba(255,255,255,0.85)", fontWeight: 500,
              }}>{s}</span>
            ))}
          </div>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12, marginBottom: 28 }}>
        {stats.map((s) => (
          <div key={s.value} style={{
            background: "#fff", border: "1px solid #e8ede9",
            borderRadius: 12, padding: "16px 20px", textAlign: "center",
          }}>
            <div style={{ fontSize: 26, fontWeight: 700, color: "#0F6E56", lineHeight: 1 }}>{s.value}</div>
            <div style={{ fontSize: 12, color: "#666", marginTop: 4 }}>{s.label}</div>
          </div>
        ))}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 14, marginBottom: 28 }}>
        {features.map((f) => (
          <div key={f.title} style={{
            background: "#fff", border: "1px solid #e8ede9",
            borderRadius: 14, padding: "22px 20px",
            display: "flex", flexDirection: "column",
          }}>
            <div style={{
              width: 44, height: 44, borderRadius: 10,
              background: f.bg, fontSize: 22,
              display: "flex", alignItems: "center", justifyContent: "center",
              marginBottom: 14,
            }}>{f.icon}</div>
            <div style={{ fontWeight: 600, fontSize: 15, marginBottom: 8 }}>{f.title}</div>
            <div style={{ fontSize: 13, color: "#555", lineHeight: 1.6, flex: 1 }}>{f.desc}</div>
            <Link href={f.href} style={{
              marginTop: 16, fontSize: 13, fontWeight: 600,
              color: f.color, textDecoration: "none",
            }}>{f.cta} →</Link>
          </div>
        ))}
      </div>

      <div style={{ background: "#fff", border: "1px solid #e8ede9", borderRadius: 14, padding: "20px 24px" }}>
        <div style={{ fontSize: 13, fontWeight: 600, color: "#333", marginBottom: 12 }}>Tech Stack</div>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
          {["Python 3.11","FastAPI","scikit-learn","SMOTE","Random Forest","A* Search","Haversine","Pydantic","structlog","pytest","Docker","Next.js","TypeScript"].map((t) => (
            <span key={t} style={{
              background: "#f3f8f5", border: "1px solid #d1e8de",
              color: "#0F6E56", fontSize: 12, fontWeight: 500,
              borderRadius: 6, padding: "4px 10px",
            }}>{t}</span>
          ))}
        </div>
      </div>
    </div>
  );
}
