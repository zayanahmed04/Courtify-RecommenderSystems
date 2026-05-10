"use client";
import { useState } from "react";
import { predictMatch, MatchPrediction } from "@/services/api";

const SPORTS  = ["Padel", "Cricket", "Football", "Badminton", "Basketball"];
const STYLES  = ["Aggressive", "Balanced", "Defensive"];
const AGES    = ["Teen", "Young Adult", "Adult", "Senior"];
const ZONES   = ["North", "South", "Central", "East", "West"];

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <label>{label}</label>
      {children}
    </div>
  );
}

function RangeField({ label, id, min, max, step = 1, value, suffix = "", onChange }: {
  label: string; id: string; min: number; max: number; step?: number;
  value: number; suffix?: string; onChange: (v: number) => void;
}) {
  return (
    <div>
      <label htmlFor={id}>
        {label}: <span style={{ color: "#0F6E56", fontWeight: 600 }}>{value}{suffix}</span>
      </label>
      <input
        id={id} type="range"
        min={min} max={max} step={step} value={value}
        onChange={(e) => onChange(Number(e.target.value))}
      />
    </div>
  );
}

const COMPAT_STYLE: Record<string, { bg: string; border: string; text: string; bar: string }> = {
  High: { bg: "#e8f5ef", border: "#a8d8bc", text: "#085041", bar: "#0F6E56" },
  Mid:  { bg: "#fef8ec", border: "#f5d98a", text: "#6b4c10", bar: "#d4a017" },
  Low:  { bg: "#fdf0f0", border: "#f5c6c6", text: "#7a2020", bar: "#c0392b" },
};

export default function MatchmakingPage() {
  const [sport,       setSport]       = useState("Padel");
  const [style,       setStyle]       = useState("Balanced");
  const [age,         setAge]         = useState("Young Adult");
  const [zone,        setZone]        = useState("South");
  const [skill,       setSkill]       = useState(7);
  const [winRate,     setWinRate]     = useState(75);
  const [gamesPlayed, setGamesPlayed] = useState(120);
  const [availability,setAvailability]= useState(10);
  const [sessionDur,  setSessionDur]  = useState(90);

  const [loading, setLoading] = useState(false);
  const [result,  setResult]  = useState<MatchPrediction | null>(null);
  const [error,   setError]   = useState("");
  const [elapsed, setElapsed] = useState<number | null>(null);

  async function handlePredict() {
    setLoading(true);
    setError("");
    setResult(null);
    const t0 = performance.now();
    try {
      const res = await predictMatch({
        skill_level:          skill,
        preferred_sport:      sport,
        play_style:           style,
        availability_hours:   availability,
        avg_session_duration: sessionDur,
        win_rate:             winRate / 100,
        age_group:            age,
        location_zone:        zone,
        games_played:         gamesPlayed,
      });
      setResult(res);
      setElapsed(Math.round(performance.now() - t0));
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  const cs = result ? COMPAT_STYLE[result.compatibility_label] ?? COMPAT_STYLE.Mid : null;

  return (
    <div>
      <div style={{ marginBottom: 28 }}>
        <h1 style={{ fontSize: 24, fontWeight: 700, color: "#111", marginBottom: 4, letterSpacing: "-0.3px" }}>
          Player Matchmaking
        </h1>
        <p style={{ fontSize: 13, color: "#666" }}>
          A Random Forest classifier predicts your match compatibility — Low, Mid, or High — based on your player profile.
        </p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "300px 1fr", gap: 20, alignItems: "start" }}>

        {/* Form */}
        <div style={{ background: "#fff", border: "1px solid #e4e9e6", borderRadius: 12, padding: "20px" }}>
          <div style={{ fontSize: 13, fontWeight: 600, color: "#333", marginBottom: 16 }}>Player profile</div>

          <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>

            <Field label="Sport">
              <select value={sport} onChange={(e) => setSport(e.target.value)}>
                {SPORTS.map((s) => <option key={s}>{s}</option>)}
              </select>
            </Field>

            <Field label="Play style">
              <select value={style} onChange={(e) => setStyle(e.target.value)}>
                {STYLES.map((s) => <option key={s}>{s}</option>)}
              </select>
            </Field>

            <Field label="Age group">
              <select value={age} onChange={(e) => setAge(e.target.value)}>
                {AGES.map((a) => <option key={a}>{a}</option>)}
              </select>
            </Field>

            <Field label="Location zone">
              <select value={zone} onChange={(e) => setZone(e.target.value)}>
                {ZONES.map((z) => <option key={z}>{z}</option>)}
              </select>
            </Field>

            <RangeField label="Skill level"         id="skill" min={1}  max={10}  value={skill}        suffix="/10" onChange={setSkill} />
            <RangeField label="Win rate"             id="wr"    min={20} max={95}  value={winRate}      suffix="%"   onChange={setWinRate} />
            <RangeField label="Games played"         id="gp"    min={1}  max={500} value={gamesPlayed}              onChange={setGamesPlayed} />
            <RangeField label="Availability"         id="av"    min={1}  max={24}  value={availability} suffix=" hrs" onChange={setAvailability} />
            <RangeField label="Session duration"     id="sd"    min={30} max={180} step={15} value={sessionDur} suffix=" min" onChange={setSessionDur} />

          </div>

          <button
            onClick={handlePredict}
            disabled={loading}
            style={{
              width: "100%", marginTop: 20,
              padding: "10px", fontSize: 14, fontWeight: 600,
              background: loading ? "#a0c4b8" : "#0F6E56",
              color: "#fff", border: "none", borderRadius: 8,
              cursor: loading ? "not-allowed" : "pointer",
            }}
          >
            {loading ? "Predicting..." : "Predict compatibility"}
          </button>
        </div>

        {/* Result */}
        <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>

          {result && cs && (
            <div style={{
              background: "#fff", border: "1px solid #e4e9e6",
              borderRadius: 12, padding: "24px",
            }}>
              {/* Class */}
              <div style={{ fontSize: 12, color: "#999", marginBottom: 8 }}>Compatibility class</div>
              <div style={{
                display: "inline-block",
                background: cs.bg, border: `1px solid ${cs.border}`,
                color: cs.text, borderRadius: 8,
                padding: "6px 16px", fontSize: 20, fontWeight: 700,
                marginBottom: 20,
              }}>
                {result.compatibility_label}
              </div>

              {/* Confidence */}
              <div style={{ marginBottom: 20 }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6, fontSize: 12 }}>
                  <span style={{ color: "#777" }}>Confidence</span>
                  <span style={{ fontWeight: 600, color: "#111" }}>{Math.round(result.confidence * 100)}%</span>
                </div>
                <div style={{ height: 6, background: "#eee", borderRadius: 3, overflow: "hidden" }}>
                  <div style={{
                    width: `${Math.round(result.confidence * 100)}%`,
                    height: "100%", borderRadius: 3,
                    background: cs.bar, transition: "width 0.6s ease",
                  }} />
                </div>
              </div>

              {/* Recommendation */}
              <div style={{
                background: "#f8faf8", border: "1px solid #e4e9e6",
                borderRadius: 8, padding: "12px 14px",
                fontSize: 13, color: "#444", lineHeight: 1.65,
              }}>
                {result.recommendation}
              </div>

              {/* Meta */}
              {elapsed !== null && (
                <div style={{ marginTop: 12, fontSize: 11, color: "#bbb" }}>
                  Inference completed in {elapsed}ms
                </div>
              )}

              {/* Feature preview */}
              <div style={{ marginTop: 20, borderTop: "1px solid #f0f0f0", paddingTop: 16 }}>
                <div style={{ fontSize: 12, color: "#999", marginBottom: 10 }}>Features sent to model</div>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 6 }}>
                  {[
                    ["skill_level", skill],
                    ["win_rate", (winRate / 100).toFixed(2)],
                    ["games_played", gamesPlayed],
                    ["experience_ratio", Math.min(gamesPlayed / 500, 1).toFixed(2)],
                    ["skill_win_interaction", ((skill / 10) * (winRate / 100)).toFixed(3)],
                    ["availability_hours", availability],
                  ].map(([k, v]) => (
                    <div key={k as string} style={{ background: "#f5f7f6", borderRadius: 6, padding: "6px 10px" }}>
                      <div style={{ fontSize: 10, color: "#999", fontFamily: "monospace" }}>{k}</div>
                      <div style={{ fontSize: 12, fontWeight: 600, color: "#333", fontFamily: "monospace" }}>{v}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {error && (
            <div style={{
              background: "#fdf0f0", border: "1px solid #f5c6c6",
              borderRadius: 10, padding: "14px 16px",
              fontSize: 13, color: "#7a2020",
            }}>
              {error}
            </div>
          )}

          {!result && !error && !loading && (
            <div style={{
              background: "#fff", border: "1px solid #e4e9e6",
              borderRadius: 12, padding: "60px 24px",
              textAlign: "center", color: "#aaa",
            }}>
              <div style={{ fontSize: 13 }}>Fill in your player profile and click Predict compatibility.</div>
            </div>
          )}

          {loading && (
            <div style={{
              background: "#fff", border: "1px solid #e4e9e6",
              borderRadius: 12, padding: "60px 24px",
              textAlign: "center", color: "#888", fontSize: 13,
            }}>
              Running prediction...
            </div>
          )}

          {/* Model info card */}
          <div style={{ background: "#fff", border: "1px solid #e4e9e6", borderRadius: 12, padding: "18px 20px" }}>
            <div style={{ fontSize: 12, fontWeight: 600, color: "#555", marginBottom: 12 }}>Model details</div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
              {[
                ["Algorithm",   "Random Forest"],
                ["Trees",       "200"],
                ["Max depth",   "10"],
                ["Balancing",   "SMOTE"],
                ["Train size",  "800 records"],
                ["Test accuracy","97%"],
              ].map(([k, v]) => (
                <div key={k} style={{ fontSize: 12 }}>
                  <span style={{ color: "#999" }}>{k}: </span>
                  <span style={{ fontWeight: 500, color: "#333" }}>{v}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
