import { apiGet, apiRequest } from "./api";
import { syntheticAnalytics, syntheticRecords } from "../mocks/fixtures";
import { sampleDocuments } from "../mocks/documents";
import type {
  AnalyticsSummary,
  RecordFilters,
  RecordsResponse,
  RollDocument,
  SourceEvidence,
} from "../types";

export function isDemoMode(): boolean {
  return import.meta.env.VITE_DEMO_MODE !== "false" &&
    import.meta.env.VITE_USE_MOCK_DATA !== "false";
}

function matches(value: string | null | undefined, query: string | undefined): boolean {
  return !query || (value ?? "").toLocaleLowerCase().includes(query.toLocaleLowerCase());
}

export async function searchRecords(
  filters: RecordFilters,
  signal?: AbortSignal,
): Promise<RecordsResponse> {
  if (!isDemoMode()) {
    return apiGet<RecordsResponse>("/records", filters as Record<string, string | number | undefined | null>, signal);
  }

  let records = [...syntheticRecords];
  records = records.filter((record) =>
    matches(record.name, filters.name) &&
    matches(record.relative_name, filters.relative_name) &&
    matches(record.voter_id, filters.voter_id) &&
    matches(record.house_number, filters.house_number) &&
    matches(record.polling_station, filters.polling_station) &&
    matches(record.document_version, filters.document_version) &&
    (!filters.gender || matches(record.gender, filters.gender)) &&
    (filters.min_age === undefined || (record.age != null && record.age >= filters.min_age)) &&
    (filters.max_age === undefined || (record.age != null && record.age <= filters.max_age)) &&
    (!filters.review_status || record.review_status === filters.review_status),
  );

  const page = Math.max(1, filters.page ?? 1);
  const pageSize = Math.max(1, filters.page_size ?? 10);
  const start = (page - 1) * pageSize;
  return {
    items: records.slice(start, start + pageSize),
    total: records.length,
    page,
    page_size: pageSize,
  };
}

export async function getEvidenceImage(
  documentId: string,
  pageNumber: number,
  signal?: AbortSignal,
): Promise<{ image_url?: string | null }> {
  if (isDemoMode()) {
    const record = syntheticRecords.find((item) => item.document_id === documentId && item.page_number === pageNumber);
    return { image_url: record?.evidence?.image_url ?? null };
  }
  return apiGet<{ image_url?: string | null }>(`/documents/${encodeURIComponent(documentId)}/pages/${pageNumber}/image`, undefined, signal);
}

export async function getPageEvidence(
  evidence: SourceEvidence,
  signal?: AbortSignal,
): Promise<{ image_url?: string | null }> {
  if (isDemoMode()) return { image_url: evidence.image_url ?? null };
  return apiGet<{ image_url?: string | null }>(
    `/evidence?url=${encodeURIComponent(evidence.image_url || "")}`,
    undefined,
    signal,
  );
}

export async function listDocuments(signal?: AbortSignal): Promise<RollDocument[]> {
  if (isDemoMode()) return [...sampleDocuments];
  return apiGet<RollDocument[]>("/documents", undefined, signal);
}

export async function uploadDocument(file: File, signal?: AbortSignal): Promise<RollDocument> {
  if (isDemoMode()) {
    const now = new Date().toISOString();
    return {
      id: `demo-upload-${Date.now()}`,
      name: file.name,
      constituency: "Uploaded demo file",
      versionLabel: "Pending demo processing",
      pageCount: 0,
      recordCount: 0,
      status: "PROCESSING",
      origin: "UPLOAD",
      updatedAt: now,
      processedPages: 0,
      note: "Simulated upload only. This PDF has not been sent to a backend or processed.",
    };
  }
  const body = new FormData();
  body.append("file", file);
  return apiRequest<RollDocument>("/documents/upload", { method: "POST", body, signal });
}

export async function getAnalytics(signal?: AbortSignal): Promise<AnalyticsSummary> {
  if (isDemoMode()) return syntheticAnalytics;
  return apiGet<AnalyticsSummary>("/analytics", undefined, signal);
}

export { apiGet };
