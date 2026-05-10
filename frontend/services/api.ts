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

export interface MatchPayload {
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

async function apiFetch<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail ?? `API error ${res.status}`);
  }

  return res.json() as Promise<T>;
}

export const searchCourts = (payload: CourtSearchPayload) =>
  apiFetch<CourtSearchResponse>("/courts/search", payload);

export const predictMatch = (payload: MatchPayload) =>
  apiFetch<MatchPrediction>("/matchmaking/predict", payload);
