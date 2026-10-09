export type ReviewStatus = 'unreviewed' | 'verified' | 'rejected' | 'needs_review';
export interface SourceEvidence { document_id: string; page_number: number; image_url?: string | null; bbox?: [number, number, number, number] | null; }
export interface VoterRecord { id: string; document_id: string; document_name?: string; document_version?: string; page_number: number; name: string; relative_name?: string | null; voter_id?: string | null; house_number?: string | null; age?: number | null; gender?: string | null; polling_station?: string | null; confidence?: number | null; review_status: ReviewStatus; evidence?: SourceEvidence | null; }
export interface RecordsResponse { items: VoterRecord[]; total: number; page: number; page_size: number; }
export interface AnalyticsSummary { dataset_name?: string; dataset_scope?: string; total_records: number; age_groups: {label:string;count:number}[]; gender_distribution: {label:string;count:number}[]; }
export interface RecordFilters { name?:string; relative_name?:string; voter_id?:string; house_number?:string; min_age?:number; max_age?:number; gender?:string; polling_station?:string; document_version?:string; review_status?: ReviewStatus; page?:number; page_size?:number; }

export type DocumentStatus = "READY" | "PROCESSING" | "NEEDS_ATTENTION" | "FAILED";
export type DocumentOrigin = "SAMPLE" | "UPLOAD";

export interface RollDocument {
  id: string;
  name: string;
  constituency: string;
  versionLabel: string;
  pageCount: number;
  recordCount: number;
  status: DocumentStatus;
  origin: DocumentOrigin;
  updatedAt: string;
  processedPages: number;
  note?: string;
}

export interface ApiEnvelope<T> {
  data: T;
  meta?: { request_id?: string };
}

export interface ApiErrorBody {
  error?: { code?: string; message?: string };
}
