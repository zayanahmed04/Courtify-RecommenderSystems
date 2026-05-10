"use client";
import { useState } from "react";
import { predictMatch, MatchPrediction } from "@/services/api";

const SPORTS  = ["Padel","Cricket","Football","Badminton","Basketball"];
const STYLES  = ["Aggressive","Balanced","Defensive"];
const AGES    = ["Teen","Young Adult","Adult","Senior"];
const ZONES   = ["North","South","Central","East","West"];

const COMPAT_COLORS: Record<string, { bg: string; color: string; border: string }> = {
  High: { bg: "#E1F5EE", color: "#085041", border: "#9FE1CB" },
  Mid:  { bg: "#FAEEDA", color: "#633806", border: "#FAC775" },
  Low:  { bg: "#FCEBEB", color: "#501313", border: "#F7C1C1" },
};

function Slider({ label, id, min, max, step = 1, value, onChange, unit = "" }: {
  label: string; id: string; min: number; max: number; step?: number;
  value: number; onChange: (v: number) => void; unit?: string;
}) {
  return (
    <div>
      <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#555", marginBottom: 8, textTransform: "uppercase", letterSpacing: "0.5px" }}>
        {label}: <span style={{ color: "#0F6E56" }}>{value}{unit}</span>
      </label>
      <input type="range" id={id} min={min} max={max} step={step} value={value}
        onChange={(e) => onChange(Number(e.target.value))} />
    </div>
  );
}

function Select({ label, value, options, onChange }: { label: string; value: string; options: string[]; onChange: (v: string) => void }) {
  return (
    <div>
      <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#555", marginBottom: 6, textTransform: "uppercase", letterSpacing: "0.5px" }}>{label}</label>
      <select value={value} onChange={(e) => onChange(e.target.value)}
        style={{ width: "100%", padding: "9px 12px", border: "1px solid #ddd", borderRadius: 8, fontSize: 14, background: "#fff" }}>
        {options.map((o) => <option key={o}>{o}</option>)}
      </select>
    </div>
  );
}

export default function MatchmakingPage() {
  const [sport, setSport]         = useState("Padel");
  const [style, setStyle]         = useState("Balanced");
  const [age, setAge]             = useState("Young Adult");
  const [zone, setZone]           = useState("South");
  const [skill, setSkill]         = useState(7);
  const [winRate, setWinRate]     = useState(75);
  const [gamesPlayed, setGamesPlayed] = useState(120);
  const [availability, setAvailability] = useState(10);
  const [sessionDur, setSessionDur]     = useState(90);

  const [loading, setLoading]   = useState(false);
  const [result, setResult]     = useState<MatchPrediction | null>(null);
  const [error, setError]       = useState("");
  const [elapsed, setElapsed]   = useState<number | null>(null);

  async function handlePredict() {
    setLoading(true);
    setError("");
    setResult(null);
    setElapsed(null);
    const t0 = performance.now();
    try {
      const res = await predictMatch({
        skill_level: skill,
        preferred_sport: sport,
        play_style: style,
        availability_hours: availability,
        avg_session_duration: sessionDur,
        win_rate: winRate / 100,
        age_group: age,
        location_zone: zone,
        games_played: gamesPlayed,
      });
      setResult(res);
      setElapsed(Math.round(performance.now() - t0));
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  const colors = result ? COMPAT_COLORS[result.compatibility_label] ?? COMPAT_COLORS.Mid : null;

  return (
    <div>
      <div style={{ marginBottom: 24 }}>
        <h1 style={{ fontSize: 24, fontWeight: 700, marginBottom: 4 }}>Player Matchmaking</h1>
        <p style={{ fontSize: 14, color: "#555" }}>
          Random Forest classifier · 200 trees · SMOTE balanced · 97% accuracy on held-out test set
        </p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, alignItems: "start" }}>
        {/* Form */}
        <div style={{ background: "#fff", border: "1px solid #e8ede9", borderRadius: 14, padding: "24px" }}>
          <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 16, color: "#333" }}>Player Profile</div>
          <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
            <Select label="Sport"      value={sport} options={SPORTS} onChange={setSport} />
            <Select label="Play Style" value={style} options={STYLES} onChange={setStyle} />
            <Select label="Age Group"  value={age}   options={AGES}   onChange={setAge} />
            <Select label="Zone"       value={zone}  options={ZONES}  onChange={setZone} />
            <Slider label="Skill Level"       id="skill" min={1}  max={10}  value={skill}        onChange={setSkill}        unit="/10" />
            <Slider label="Win Rate"          id="wr"    min={20} max={95}  value={winRate}      onChange={setWinRate}      unit="%" />
            <Slider label="Games Played"      id="gp"    min={1}  max={500} value={gamesPlayed}  onChange={setGamesPlayed} />
            <Slider label="Availability"      id="av"    min={1}  max={24}  value={availability} onChange={setAvailability} unit=" hrs" />
            <Slider label="Session Duration"  id="sd"    min={30} max={180} step={15} value={sessionDur} onChange={setSessionDur} unit=" min" />
          </div>
          <button
            onClick={handlePredict}
            disabled={loading}
            style={{
              width: "100%", padding: "12px", marginTop: 20,
              fontSize: 14, fontWeight: 600,
              background: loading ? "#9FE1CB" : "#0F6E56",
              color: "#fff", border: "none", borderRadius: 10,
              cursor: loading ? "not-allowed" : "pointer",
            }}
          >
            {loading ? "⏳ Running inference..." : "🤖 Predict Compatibility"}
          </button>
        </div>

        {/* Result Panel */}
        <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
          {result && colors && (
            <div style={{ background: "#fff", border: "1px solid #e8ede9", borderRadius: 14, padding: "24px", animation: "fadeIn 0.3s ease" }}>
              <style>{`@keyframes fadeIn { from { opacity:0; transform:translateY(8px) } to { opacity:1; transform:none } }`}</style>
              <div style={{ fontSize: 12, fontWeight: 600, color: "#888", textTransform: "uppercase", letterSpacing: "0.5px", marginBottom: 8 }}>Compatibility Class</div>
              <div style={{
                display: "inline-flex", alignItems: "center", gap: 10,
                background: colors.bg, border: `1px solid ${colors.border}`,
                borderRadius: 12, padding: "10px 18px", marginBottom: 16,
              }}>
                <span style={{ fontSize: 28 }}>
                  {result.compatibility_label === "High" ? "🏆" : result.compatibility_label === "Mid" ? "⚔️" : "📚"}
                </span>
                <span style={{ fontSize: 24, fontWeight: 700, color: colors.color }}>{result.compatibility_label}</span>
              </div>

              <div style={{ marginBottom: 16 }}>
                <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, color: "#666", marginBottom: 6 }}>
                  <span>Confidence</span>
                  <span style={{ fontWeight: 600, color: "#0F6E56" }}>{Math.round(result.confidence * 100)}%</span>
                </div>
                <div style={{ height: 8, background: "#e8ede9", borderRadius: 4, overflow: "hidden" }}>
                  <div style={{
                    width: `${Math.round(result.confidence * 100)}%`,
                    height: "100%",
                    background: result.compatibility_label === "High" ? "#0F6E56" : result.compatibility_label === "Mid" ? "#EF9F27" : "#E24B4A",
                    borderRadius: 4, transition: "width 0.8s ease",
                  }} />
                </div>
              </div>

              <div style={{ background: "#f8faf9", borderRadius: 10, padding: "12px 14px", fontSize: 13, color: "#444", lineHeight: 1.6 }}>
                {result.recommendation}
              </div>

              {elapsed !== null && (
                <div style={{ fontSize: 11, color: "#aaa", marginTop: 10, textAlign: "right" }}>
                  Inference in {elapsed}ms
                </div>
              )}
            </div>
          )}

          {error && (
            <div style={{ background: "#FCEBEB", border: "1px solid #F7C1C1", borderRadius: 10, padding: "14px", fontSize: 13, color: "#A32D2D" }}>
              ❌ {error}
            </div>
          )}

          {!result && !error && (
            <div style={{ background: "#fff", border: "1px solid #e8ede9", borderRadius: 14, padding: "40px 24px", textAlign: "center", color: "#aaa" }}>
              <div style={{ fontSize: 40, marginBottom: 10 }}>🤖</div>
              <div style={{ fontSize: 14 }}>Fill in the player profile and hit Predict</div>
            </div>
          )}

          {/* Pipeline info */}
          <div style={{ background: "#fff", border: "1px solid #e8ede9", borderRadius: 14, padding: "18px 20px" }}>
            <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 12 }}>ML Pipeline</div>
            {[
              ["🔧", "Feature Engineering", "experience_ratio + skill×win interaction"],
              ["🔠", "Label Encoding",       "sport, style, age, zone → integers"],
              ["📏", "MinMax Scaling",       "skill, win_rate, duration, games → [0,1]"],
              ["⚖️",  "SMOTE",               "Synthetic minority oversampling on training set"],
              ["🌲", "Random Forest",        "200 trees, max_depth=10, class_weight=balanced"],
              ["📊", "predict_proba()",      "Returns class + confidence from RF leaf votes"],
            ].map(([icon, title, desc]) => (
              <div key={title as string} style={{ display: "flex", gap: 10, marginBottom: 8, alignItems: "flex-start" }}>
                <span style={{ fontSize: 14, flexShrink: 0 }}>{icon}</span>
                <div style={{ fontSize: 12 }}>
                  <span style={{ fontWeight: 600 }}>{title}</span>
                  <span style={{ color: "#666" }}> — {desc}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
