export default function HowItWorksPage() {
  return (
    <div>
      <div style={{ marginBottom: 28 }}>
        <h1 style={{ fontSize: 24, fontWeight: 700, marginBottom: 4 }}>How It Works</h1>
        <p style={{ fontSize: 14, color: "#555" }}>
          System architecture, algorithm explanations, and production engineering decisions.
        </p>
      </div>

      {/* A* Section */}
      <Section
        color="#0F6E56" bg="#E1F5EE"
        icon="🎯"
        title="A* Court Search Engine"
        subtitle="app/services/court_search/astar_engine.py"
      >
        <p style={{ fontSize: 14, color: "#444", lineHeight: 1.7, marginBottom: 16 }}>
          Every court is evaluated by a multi-factor heuristic <Code>h(n)</Code> that scores across three
          normalised dimensions. The engine uses Python&apos;s <Code>heapq</Code> min-heap — the best court
          is always at the top. Hard filters eliminate bad candidates <em>before</em> scoring runs.
        </p>

        <CodeBlock>{`# heuristic.py
def evaluate(self, player_location, court, budget):
    distance  = haversine_distance(*player_location, court.lat, court.lon)
    norm_dist  = clamp(distance / 50)          # 50km ceiling
    norm_price = clamp(court.price / budget)
    norm_rating = 1 - court.rating / 5         # inverted — higher = better

    return (
        self.weights.distance * norm_dist   # 0.5
      + self.weights.price    * norm_price  # 0.3
      + self.weights.rating   * norm_rating # 0.2
    )`}</CodeBlock>

        <Steps color="#0F6E56" bg="#E1F5EE" items={[
          ["Hard filter", "Remove courts of wrong sport or over budget — O(n)"],
          ["Score h(n)", "Compute heuristic per candidate via Haversine formula"],
          ["heapq.heappush", "Push (score, court_id, court) into min-heap"],
          ["heapq.heappop", "Pop top-N; closed set prevents re-evaluation"],
          ["Return ranked list", "CourtSearchResponse with scores, distances, slots"],
        ]} />

        <InfoRow items={[
          ["5ms", "@ 5,000 courts"],
          ["Deterministic", "Same query = same order"],
          ["Tunable", "Weights per-request"],
        ]} color="#0F6E56" bg="#E1F5EE" />
      </Section>

      {/* ML Section */}
      <Section
        color="#185FA5" bg="#E6F1FB"
        icon="🤖"
        title="ML Matchmaking Pipeline"
        subtitle="app/services/matchmaking/"
      >
        <p style={{ fontSize: 14, color: "#444", lineHeight: 1.7, marginBottom: 16 }}>
          A Random Forest classifier (200 trees, max depth 10) predicts match compatibility.
          Trained on 1,000 synthetic player records. SMOTE handles class imbalance before training.
          The preprocessor is stateful — fitted once, serialised to disk, used read-only at inference.
        </p>

        <CodeBlock>{`# feature_engineering.py
def add_derived_features(df):
    df["experience_ratio"]     = (df["games_played"] / 500).clip(0, 1)
    df["skill_win_interaction"] = (df["skill_level"] / 10) * df["win_rate"]
    return df

# trainer.py — SMOTE before fit
smote = SMOTE(random_state=42)
X_train_bal, y_train_bal = smote.fit_resample(X_train, y_train)
model.fit(X_train_bal, y_train_bal)   # 97% accuracy`}</CodeBlock>

        <Steps color="#185FA5" bg="#E6F1FB" items={[
          ["Feature Engineering",  "Add experience_ratio, skill×win_rate interaction"],
          ["LabelEncoder",         "Encode sport, style, age, zone → integers"],
          ["MinMaxScaler",         "Scale numerical features to [0, 1]"],
          ["SMOTE",                "Synthetic minority oversampling on training split only"],
          ["Random Forest fit",    "200 trees, class_weight=balanced, n_jobs=-1"],
          ["predict_proba()",      "Returns class index + max probability as confidence"],
        ]} />

        <InfoRow items={[
          ["97%", "Test accuracy"],
          ["3 classes", "Low / Mid / High"],
          ["SMOTE", "Class balancing"],
        ]} color="#185FA5" bg="#E6F1FB" />
      </Section>

      {/* API Section */}
      <Section
        color="#534AB7" bg="#EEEDFE"
        icon="⚡"
        title="FastAPI Production Backend"
        subtitle="app/api/ + app/main.py"
      >
        <p style={{ fontSize: 14, color: "#444", lineHeight: 1.7, marginBottom: 16 }}>
          Stateless FastAPI backend. All inputs validated by Pydantic models with field constraints.
          Domain exceptions map cleanly to HTTP status codes. Lazy model loading means the API starts
          even before training — it returns a clear 503 instead of crashing.
        </p>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10, marginBottom: 16 }}>
          {[
            { method: "GET",  path: "/health",              code: "200", desc: "Status + model ready flag" },
            { method: "POST", path: "/courts/search",       code: "200/404/422", desc: "A* recommendations" },
            { method: "POST", path: "/matchmaking/predict", code: "200/422/503", desc: "RF compatibility" },
          ].map((r) => (
            <div key={r.path} style={{ background: "#fff", border: "1px solid #e8ede9", borderRadius: 10, padding: "12px 14px" }}>
              <div style={{ display: "flex", gap: 6, alignItems: "center", marginBottom: 6 }}>
                <span style={{
                  fontSize: 10, fontWeight: 700, padding: "2px 6px", borderRadius: 4,
                  background: r.method === "GET" ? "#E1F5EE" : "#EEEDFE",
                  color: r.method === "GET" ? "#085041" : "#3C3489",
                }}>{r.method}</span>
                <code style={{ fontSize: 11, color: "#333" }}>{r.path}</code>
              </div>
              <div style={{ fontSize: 11, color: "#666" }}>{r.desc}</div>
              <div style={{ fontSize: 10, color: "#aaa", marginTop: 4 }}>HTTP {r.code}</div>
            </div>
          ))}
        </div>

        <Steps color="#534AB7" bg="#EEEDFE" items={[
          ["Pydantic validation",    "Field constraints — bad input returns 422 automatically"],
          ["Dependency injection",   "Depends() wires courts list + engines per-request"],
          ["Exception mapping",      "NoCourtsFoundError → 404, ModelNotTrainedError → 503"],
          ["structlog",              "JSON logs in production, human-readable in dev mode"],
          ["Docker HEALTHCHECK",     "Polls /health every 30s, restarts on failure"],
        ]} />
      </Section>

      {/* Tests Section */}
      <Section
        color="#3B6D11" bg="#EAF3DE"
        icon="✅"
        title="Test Suite — 47/47 Passing"
        subtitle="tests/"
      >
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
          {[
            { file: "test_heuristic.py", n: 11, desc: "Haversine, normalize, clamp, weighted_sum" },
            { file: "test_astar.py",     n: 12, desc: "Search results, sport/budget filters, score ordering" },
            { file: "test_matchmaking.py",n: 10,desc: "Dataset, feature engineering, preprocessor" },
            { file: "test_api.py",       n: 12, desc: "All endpoints, error codes, validation" },
            { file: "test_performance.py",n: 5, desc: "A* latency at 100/500/1000/5000 courts, determinism" },
          ].map((t) => (
            <div key={t.file} style={{ display: "flex", gap: 10, alignItems: "flex-start" }}>
              <div style={{
                width: 28, height: 28, borderRadius: 6,
                background: "#EAF3DE", color: "#3B6D11",
                fontSize: 11, fontWeight: 700,
                display: "flex", alignItems: "center", justifyContent: "center",
                flexShrink: 0,
              }}>{t.n}</div>
              <div>
                <div style={{ fontSize: 12, fontWeight: 600, color: "#333", fontFamily: "monospace" }}>{t.file}</div>
                <div style={{ fontSize: 12, color: "#666" }}>{t.desc}</div>
              </div>
            </div>
          ))}
        </div>
      </Section>
    </div>
  );
}

function Section({ color, bg, icon, title, subtitle, children }: {
  color: string; bg: string; icon: string;
  title: string; subtitle: string; children: React.ReactNode;
}) {
  return (
    <div style={{ background: "#fff", border: "1px solid #e8ede9", borderRadius: 14, padding: "24px", marginBottom: 16 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 16 }}>
        <div style={{
          width: 42, height: 42, borderRadius: 10, background: bg,
          display: "flex", alignItems: "center", justifyContent: "center", fontSize: 20, flexShrink: 0,
        }}>{icon}</div>
        <div>
          <div style={{ fontWeight: 700, fontSize: 16, color: "#1a1a1a" }}>{title}</div>
          <code style={{ fontSize: 11, color: color }}>{subtitle}</code>
        </div>
      </div>
      {children}
    </div>
  );
}

function Code({ children }: { children: React.ReactNode }) {
  return <code style={{ background: "#f3f3f3", padding: "1px 5px", borderRadius: 4, fontSize: 12, fontFamily: "monospace" }}>{children}</code>;
}

function CodeBlock({ children }: { children: string }) {
  return (
    <pre style={{
      background: "#1a1a2e", color: "#a8d8a8", fontFamily: "monospace",
      fontSize: 12, borderRadius: 10, padding: "14px 16px",
      overflowX: "auto", lineHeight: 1.7, marginBottom: 16,
      whiteSpace: "pre-wrap",
    }}>
      {children}
    </pre>
  );
}

function Steps({ color, bg, items }: { color: string; bg: string; items: [string, string][] }) {
  return (
    <div style={{ marginBottom: 16 }}>
      {items.map(([title, desc], i) => (
        <div key={title} style={{ display: "flex", gap: 10, marginBottom: 8, alignItems: "flex-start" }}>
          <div style={{
            width: 20, height: 20, borderRadius: "50%",
            background: bg, color: color,
            fontSize: 10, fontWeight: 700,
            display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, marginTop: 1,
          }}>{i + 1}</div>
          <div style={{ fontSize: 13 }}>
            <span style={{ fontWeight: 600 }}>{title}</span>
            <span style={{ color: "#555" }}> — {desc}</span>
          </div>
        </div>
      ))}
    </div>
  );
}

function InfoRow({ items, color, bg }: { items: [string, string][]; color: string; bg: string }) {
  return (
    <div style={{ display: "flex", gap: 10 }}>
      {items.map(([val, label]) => (
        <div key={label} style={{ background: bg, borderRadius: 8, padding: "8px 14px", flex: 1, textAlign: "center" }}>
          <div style={{ fontSize: 16, fontWeight: 700, color }}>{val}</div>
          <div style={{ fontSize: 11, color: "#666", marginTop: 2 }}>{label}</div>
        </div>
      ))}
    </div>
  );
}
