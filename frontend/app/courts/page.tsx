"use client";
import { useState } from "react";
import { searchCourts, CourtResult } from "@/services/api";

const SPORTS = ["Padel", "Cricket", "Football", "Badminton", "Basketball"];

// Real zone coordinates matching Karachi areas where the courts CSV was generated
const ZONES: Record<string, [number, number]> = {
  North:   [24.930, 67.055],
  South:   [24.800, 67.025],
  Central: [24.860, 67.000],
  East:    [24.832, 67.130],
  West:    [24.883, 66.995],
};

const BUDGETS = [500, 600, 800, 1000, 1200, 1500, 2000, 2500];

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <label>{label}</label>
      {children}
    </div>
  );
}

function ResultCard({ result, rank }: { result: CourtResult; rank: number }) {
  const matchPct = Math.round((1 - result.score) * 100);
  return (
    <div style={{
      background: "#fff",
      border: rank === 1 ? "1.5px solid #0F6E56" : "1px solid #e4e9e6",
      borderRadius: 12, padding: "18px 20px",
      display: "flex", gap: 16, alignItems: "flex-start",
    }}>
      {/* Rank */}
      <div style={{
        width: 32, height: 32, borderRadius: 8,
        background: rank === 1 ? "#0F6E56" : "#f0f0f0",
        color: rank === 1 ? "#fff" : "#888",
        fontSize: 13, fontWeight: 700,
        display: "flex", alignItems: "center", justifyContent: "center",
        flexShrink: 0,
      }}>
        {rank}
      </div>

      {/* Info */}
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ fontWeight: 600, fontSize: 15, color: "#111", marginBottom: 6 }}>
          {result.court}
        </div>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 16, marginBottom: 12 }}>
          {[
            { label: "Distance",   val: result.distance_km != null ? `${result.distance_km} km` : "—" },
            { label: "Price",      val: `PKR ${result.price}/hr` },
            { label: "Rating",     val: `${result.rating.toFixed(1)} / 5` },
            { label: "Slots",      val: result.available_slots.slice(0, 3).join(", ") || "—" },
          ].map(({ label, val }) => (
            <div key={label}>
              <div style={{ fontSize: 11, color: "#999", marginBottom: 1 }}>{label}</div>
              <div style={{ fontSize: 13, fontWeight: 500, color: "#333" }}>{val}</div>
            </div>
          ))}
        </div>
        {/* Match bar */}
        <div>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
            <span style={{ fontSize: 11, color: "#999" }}>Match score (lower h(n) = better)</span>
            <span style={{ fontSize: 11, fontWeight: 600, color: "#0F6E56" }}>{matchPct}%</span>
          </div>
          <div style={{ height: 4, background: "#e8ede9", borderRadius: 2, overflow: "hidden" }}>
            <div style={{
              width: `${matchPct}%`, height: "100%",
              background: "#0F6E56", borderRadius: 2,
            }} />
          </div>
        </div>
      </div>

      {/* h(n) score */}
      <div style={{ textAlign: "right", flexShrink: 0 }}>
        <div style={{ fontSize: 10, color: "#aaa", marginBottom: 2 }}>h(n)</div>
        <div style={{ fontSize: 18, fontWeight: 700, color: "#0F6E56" }}>{result.score}</div>
      </div>
    </div>
  );
}

export default function CourtsPage() {
  const [sport, setSport]         = useState("Padel");
  const [budget, setBudget]       = useState(1500);
  const [zone, setZone]           = useState("Central");
  const [maxResults, setMaxResults] = useState(5);

  const [loading, setLoading]   = useState(false);
  const [results, setResults]   = useState<CourtResult[]>([]);
  const [error, setError]       = useState("");
  const [meta, setMeta]         = useState<{ elapsed: number; found: number } | null>(null);

  async function handleSearch() {
    setLoading(true);
    setError("");
    setResults([]);
    setMeta(null);
    const t0 = performance.now();
    try {
      const res = await searchCourts({
        sport,
        budget,
        location: ZONES[zone],
        max_results: maxResults,
      });
      setResults(res.recommendations);
      setMeta({ elapsed: Math.round(performance.now() - t0), found: res.total_found });
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      {/* Page header */}
      <div style={{ marginBottom: 28 }}>
        <h1 style={{ fontSize: 24, fontWeight: 700, color: "#111", marginBottom: 4, letterSpacing: "-0.3px" }}>
          Find Courts
        </h1>
        <p style={{ fontSize: 13, color: "#666" }}>
          Courts are ranked by A* heuristic — h(n) = 0.5 × distance + 0.3 × price + 0.2 × rating. Lower score is a better match.
        </p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "280px 1fr", gap: 20, alignItems: "start" }}>

        {/* Sidebar form */}
        <div style={{ background: "#fff", border: "1px solid #e4e9e6", borderRadius: 12, padding: "20px" }}>
          <div style={{ fontSize: 13, fontWeight: 600, color: "#333", marginBottom: 16 }}>Search filters</div>

          <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>

            <Field label="Sport">
              <select value={sport} onChange={(e) => setSport(e.target.value)}>
                {SPORTS.map((s) => <option key={s}>{s}</option>)}
              </select>
            </Field>

            <Field label="Your zone">
              <select value={zone} onChange={(e) => setZone(e.target.value)}>
                {Object.keys(ZONES).map((z) => <option key={z}>{z}</option>)}
              </select>
            </Field>

            <Field label="Max budget (PKR/hr)">
              <select value={budget} onChange={(e) => setBudget(Number(e.target.value))}>
                {BUDGETS.map((b) => <option key={b} value={b}>PKR {b}</option>)}
              </select>
            </Field>

            <Field label={`Results to show: ${maxResults}`}>
              <input
                type="range" min={1} max={10} step={1}
                value={maxResults}
                onChange={(e) => setMaxResults(Number(e.target.value))}
              />
            </Field>

          </div>

          <button
            onClick={handleSearch}
            disabled={loading}
            style={{
              width: "100%", marginTop: 20,
              padding: "10px", fontSize: 14, fontWeight: 600,
              background: loading ? "#a0c4b8" : "#0F6E56",
              color: "#fff", border: "none", borderRadius: 8,
              cursor: loading ? "not-allowed" : "pointer",
              transition: "background 0.12s",
            }}
          >
            {loading ? "Searching..." : "Search"}
          </button>

          {/* Zone coords info */}
          <div style={{ marginTop: 14, padding: "10px 12px", background: "#f5f7f6", borderRadius: 8 }}>
            <div style={{ fontSize: 11, color: "#888", marginBottom: 4 }}>Location used</div>
            <div style={{ fontSize: 11, fontFamily: "monospace", color: "#555" }}>
              {ZONES[zone][0].toFixed(4)}, {ZONES[zone][1].toFixed(4)}
            </div>
          </div>
        </div>

        {/* Results */}
        <div>
          {/* Status bar */}
          {meta && !error && (
            <div style={{
              fontSize: 12, color: "#0F6E56",
              background: "#e8f5ef", border: "1px solid #c2dfd4",
              borderRadius: 8, padding: "8px 12px", marginBottom: 14,
            }}>
              Found {meta.found} court{meta.found !== 1 ? "s" : ""} in {meta.elapsed}ms — sorted by h(n) ascending
            </div>
          )}

          {error && (
            <div style={{
              fontSize: 13, color: "#7a2020",
              background: "#fdf0f0", border: "1px solid #f5c6c6",
              borderRadius: 8, padding: "10px 14px", marginBottom: 14,
            }}>
              {error}
            </div>
          )}

          {results.length > 0 && (
            <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
              {results.map((r, i) => (
                <ResultCard key={`${r.court}-${i}`} result={r} rank={i + 1} />
              ))}
            </div>
          )}

          {!loading && results.length === 0 && !error && (
            <div style={{
              background: "#fff", border: "1px solid #e4e9e6",
              borderRadius: 12, padding: "60px 24px",
              textAlign: "center", color: "#aaa",
            }}>
              <div style={{ fontSize: 13 }}>Select your sport, zone, and budget — then hit Search.</div>
            </div>
          )}

          {loading && (
            <div style={{
              background: "#fff", border: "1px solid #e4e9e6",
              borderRadius: 12, padding: "60px 24px",
              textAlign: "center", color: "#888", fontSize: 13,
            }}>
              Running A* search...
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
