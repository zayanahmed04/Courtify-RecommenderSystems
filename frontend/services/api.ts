const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export interface CourtSearchPayload {
  sport: string;
  budget: number;
  location: [number, number];
  max_results?: number;
}

export interface CourtResult {
  court: string;
  score: number;
  rating: number;
  price: number;
  distance_km: number | null;
  available_slots: string[];
}

export interface CourtSearchResponse {
  query_sport: string;
  budget: number;
  total_found: number;
  recommendations: CourtResult[];
}

export interface PlayerMatchPayload {
  skill_level: number;
  preferred_sport: string;
  play_style: string;
  availability_hours: number;
  avg_session_duration: number;
  win_rate: number;
  age_group: string;
  location_zone: string;
  games_played: number;
}

export interface MatchPrediction {
  compatibility_class: number;
  compatibility_label: string;
  confidence: number;
  recommendation: string;
}

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
  model_ready: boolean;
}

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail ?? `API error ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export const searchCourts = (payload: CourtSearchPayload) =>
  apiFetch<CourtSearchResponse>("/courts/search", {
    method: "POST",
    body: JSON.stringify(payload),
  });

export const predictMatch = (payload: PlayerMatchPayload) =>
  apiFetch<MatchPrediction>("/matchmaking/predict", {
    method: "POST",
    body: JSON.stringify(payload),
  });

export const getHealth = () => apiFetch<HealthResponse>("/health");
