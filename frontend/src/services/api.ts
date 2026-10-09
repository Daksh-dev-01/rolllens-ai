import type { ApiEnvelope, ApiErrorBody } from "../types";

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000").replace(/\/$/, "");

export class ApiError extends Error {
  status: number;
  code?: string;
  constructor(message: string, status = 0, code?: string) {
    super(message); this.name = "ApiError"; this.status = status; this.code = code;
  }
}

export function isDemoMode(): boolean {
  return import.meta.env.VITE_DEMO_MODE === "false"
    ? false
    : import.meta.env.VITE_USE_MOCK_DATA !== "false";
}

function withApiPrefix(path: string): string {
  const clean = path.startsWith("/") ? path : `/${path}`;
  return clean.startsWith("/api/v1/") || clean === "/api/v1"
    ? clean
    : `/api/v1${clean}`;
}

export async function apiRequest<T>(path: string, init?: RequestInit): Promise<T> {
  if (isDemoMode()) throw new ApiError("This action is not connected in sample mode.", 501, "DEMO_MODE");
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}${withApiPrefix(path)}`, {
      ...init,
      headers: {
        ...(init?.body && !(init.body instanceof FormData) ? { "Content-Type": "application/json" } : {}),
        Accept: "application/json",
        ...init?.headers,
      },
    });
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") throw error;
    throw new ApiError("Could not reach the RollLens API. Check that the backend is running.", 0, "NETWORK_ERROR");
  }
  const responseText = await response.text();
  let payload: (ApiEnvelope<T> & ApiErrorBody & { detail?: unknown }) | undefined;
  if (responseText.trim()) {
    try {
      payload = JSON.parse(responseText) as ApiEnvelope<T> & ApiErrorBody & { detail?: unknown };
    } catch {
      if (response.ok) throw new ApiError("Invalid JSON payload response.", response.status, "INVALID_JSON");
    }
  } else if (response.ok) {
    throw new ApiError("Empty response body.", response.status, "EMPTY_RESPONSE");
  }
  if (!response.ok) {
    const detail = typeof payload?.detail === "string" ? payload.detail : undefined;
    throw new ApiError(payload?.error?.message || detail || `Request failed (${response.status}).`, response.status, payload?.error?.code);
  }
  return (payload && typeof payload === "object" && "data" in payload ? payload.data : payload) as T;
}

export async function apiGet<T>(path: string, params?: Record<string, string | number | undefined | null>, signal?: AbortSignal): Promise<T> {
  const query = new URLSearchParams();
  Object.entries(params ?? {}).forEach(([key, value]) => {
    if (value !== undefined && value !== null && String(value).trim() !== "") query.set(key, String(value));
  });
  const suffix = query.toString();
  return apiRequest<T>(`${path}${suffix ? `${path.includes("?") ? "&" : "?"}${suffix}` : ""}`, { method: "GET", signal });
}

export function apiUrl(path: string): string { return `${API_BASE_URL}${withApiPrefix(path)}`; }