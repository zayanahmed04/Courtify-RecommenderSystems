"use client";
import { useState } from "react";
import { searchCourts, CourtResult } from "@/services/api";

const SPORTS = ["Padel", "Cricket", "Football", "Badminton", "Basketball"];
const ZONES: Record<string, [number, number]> = {
  Central: [24.8607, 67.0011],
  North:   [24.9239, 67.0621],
  South:   [24.8121, 67.0299],
  East:    [24.8324, 67.1282],
  West:    [24.8715, 66.9900],
};

function ScoreBar({ score }: { score: number }) {
  const pct = Math.round((1 - score) * 100);
  return (
    <div>
      <div style={{ fontSize: 11, color: "#888", marginBottom: 4 }}>Match Score</div>
      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
        <div style={{ flex: 1, height: 6, background: "#e8ede9", borderRadius: 3, overflow: "hidden" }}>
          <div style={{ width: `${pct}%`, height: "100%", background: "#0F6E56", borderRadius: 3, transition: "width 0.6s ease" }} />
        </div>
        <span style={{ fontSize: 12, fontWeight: 600, color: "#0F6E56", minWidth: 32 }}>{pct}%</span>
      </div>
    </div>
  );
}

function CourtCard({ result, rank }: { result: CourtResult; rank: number }) {
  const medals = ["🥇", "🥈", "🥉"];
  return (
    <div style={{
      background: "#fff",
      border: rank === 1 ? "1.5px solid #1D9E75" : "1px solid #e8ede9",
      borderRadius: 14,
      padding: "18px 20px",
      display: "flex",
      gap: 16,
      alignItems: "flex-start",
      animation: "fadeUp 0.3s ease forwards",
      animationDelay: `${(rank - 1) * 80}ms`,
      opacity: 0,
    }}>
      <div style={{
        width: 40, height: 40, borderRadius: 10,
        background: rank === 1 ? "#E1F5EE" : "#f5f5f5",
        display: "flex", alignItems: "center", justifyContent: "center",
        fontSize: 18, flexShrink: 0,
      }}>
        {medals[rank - 1] ?? `#${rank}`}
      </div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ fontWeight: 600, fontSize: 15, marginBottom: 6 }}>{result.court}</div>
        <div style={{ display: "flex", gap: 16, flexWrap: "wrap", marginBottom: 10 }}>
          {[
            { icon: "📍", val: result.distance_km != null ? `${result.distance_km} km` : "—" },
            { icon: "💰", val: `PKR ${result.price}/hr` },
            { icon: "⭐", val: result.rating.toFixed(1) },
            { icon: "🕐", val: result.available_slots.slice(0, 3).join(", ") || "—" },
          ].map(({ icon, val }) => (
            <span key={val} style={{ fontSize: 12, color: "#555", display: "flex", alignItems: "center", gap: 4 }}>
              {icon} {val}
            </span>
          ))}
        </div>
        <ScoreBar score={result.score} />
      </div>
      <div style={{ textAlign: "right", flexShrink: 0 }}>
        <div style={{ fontSize: 11, color: "#888" }}>h(n)</div>
        <div style={{ fontSize: 16, fontWeight: 700, color: "#0F6E56" }}>{result.score}</div>
      </div>
    </div>
  );
}

export default function CourtsPage() {
  const [sport, setSport] = useState("Padel");
  const [budget, setBudget] = useState(1500);
  const [zone, setZone] = useState("Central");
  const [maxResults, setMaxResults] = useState(3);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<CourtResult[]>([]);
  const [error, setError] = useState("");
  const [elapsed, setElapsed] = useState<number | null>(null);

  async function handleSearch() {
    setLoading(true);
    setError("");
    setResults([]);
    setElapsed(null);
    const t0 = performance.now();
    try {
      const res = await searchCourts({
        sport,
        budget,
        location: ZONES[zone],
        max_results: maxResults,
      });
      setResults(res.recommendations);
      setElapsed(Math.round(performance.now() - t0));
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <style>{`@keyframes fadeUp { from { opacity:0; transform:translateY(10px) } to { opacity:1; transform:none } }`}</style>
      <div style={{ marginBottom: 24 }}>
        <h1 style={{ fontSize: 24, fontWeight: 700, marginBottom: 4 }}>Court Search</h1>
        <p style={{ fontSize: 14, color: "#555" }}>
          A* informed search — courts ranked by weighted heuristic h(n) = 0.5×distance + 0.3×price + 0.2×rating
        </p>
      </div>

      {/* Form */}
      <div style={{ background: "#fff", border: "1px solid #e8ede9", borderRadius: 14, padding: "24px", marginBottom: 20 }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 16 }}>
          <div>
            <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#555", marginBottom: 6, textTransform: "uppercase", letterSpacing: "0.5px" }}>Sport</label>
            <select
              value={sport}
              onChange={(e) => setSport(e.target.value)}
              style={{ width: "100%", padding: "9px 12px", border: "1px solid #ddd", borderRadius: 8, fontSize: 14, background: "#fff" }}
            >
              {SPORTS.map((s) => <option key={s}>{s}</option>)}
            </select>
          </div>
          <div>
            <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#555", marginBottom: 6, textTransform: "uppercase", letterSpacing: "0.5px" }}>Your Zone</label>
            <select
              value={zone}
              onChange={(e) => setZone(e.target.value)}
              style={{ width: "100%", padding: "9px 12px", border: "1px solid #ddd", borderRadius: 8, fontSize: 14, background: "#fff" }}
            >
              {Object.keys(ZONES).map((z) => <option key={z}>{z}</option>)}
            </select>
          </div>
          <div>
            <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#555", marginBottom: 8, textTransform: "uppercase", letterSpacing: "0.5px" }}>
              Max Budget: <span style={{ color: "#0F6E56" }}>PKR {budget}/hr</span>
            </label>
            <input type="range" min={400} max={2500} step={100} value={budget} onChange={(e) => setBudget(Number(e.target.value))} />
          </div>
          <div>
            <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#555", marginBottom: 8, textTransform: "uppercase", letterSpacing: "0.5px" }}>
              Results: <span style={{ color: "#0F6E56" }}>{maxResults}</span>
            </label>
            <input type="range" min={1} max={5} step={1} value={maxResults} onChange={(e) => setMaxResults(Number(e.target.value))} />
          </div>
        </div>

        <button
          onClick={handleSearch}
          disabled={loading}
          style={{
            width: "100%", padding: "12px", fontSize: 14, fontWeight: 600,
            background: loading ? "#9FE1CB" : "#0F6E56",
            color: "#fff", border: "none", borderRadius: 10,
            cursor: loading ? "not-allowed" : "pointer",
            transition: "background 0.15s",
          }}
        >
          {loading ? "⏳ Running A* Search..." : "🔍 Run A* Search"}
        </button>
      </div>

      {/* Status */}
      {(elapsed !== null || error) && (
        <div style={{
          padding: "10px 14px", borderRadius: 8, marginBottom: 16, fontSize: 13,
          background: error ? "#FCEBEB" : "#E1F5EE",
          color: error ? "#A32D2D" : "#085041",
          border: `1px solid ${error ? "#F7C1C1" : "#9FE1CB"}`,
        }}>
          {error
            ? `❌ ${error}`
            : `✅ Found ${results.length} courts in ${elapsed}ms · Sorted by h(n) score (lower = better match)`}
        </div>
      )}

      {/* Results */}
      {results.length > 0 && (
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {results.map((r, i) => <CourtCard key={r.court} result={r} rank={i + 1} />)}
        </div>
      )}

      {!loading && results.length === 0 && !error && (
        <div style={{ textAlign: "center", padding: "48px 0", color: "#aaa" }}>
          <div style={{ fontSize: 40, marginBottom: 10 }}>🏟️</div>
          <div style={{ fontSize: 14 }}>Configure your search above and hit Run A* Search</div>
        </div>
      )}

      {/* Algorithm explanation */}
      <div style={{ marginTop: 24, background: "#f8faf9", border: "1px solid #e8ede9", borderRadius: 14, padding: "18px 20px" }}>
        <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 10 }}>How the A* Engine Works</div>
        {[
          ["1", "Hard filter", "Remove courts of wrong sport or exceeding budget — O(n)"],
          ["2", "Score h(n)", "Compute heuristic for each candidate using Haversine distance"],
          ["3", "Priority queue", "Push all scored courts into a min-heap"],
          ["4", "Pop top-N", "Extract best N courts; closed set prevents re-evaluation"],
        ].map(([num, title, desc]) => (
          <div key={num} style={{ display: "flex", gap: 10, marginBottom: 8, alignItems: "flex-start" }}>
            <div style={{
              width: 20, height: 20, borderRadius: "50%",
              background: "#E1F5EE", color: "#0F6E56",
              fontSize: 11, fontWeight: 700,
              display: "flex", alignItems: "center", justifyContent: "center",
              flexShrink: 0, marginTop: 1,
            }}>{num}</div>
            <div style={{ fontSize: 13 }}>
              <span style={{ fontWeight: 600 }}>{title}</span>
              <span style={{ color: "#555" }}> — {desc}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
