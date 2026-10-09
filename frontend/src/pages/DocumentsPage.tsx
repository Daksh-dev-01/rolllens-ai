import { useEffect, useMemo, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowDownToLine, ArrowRight, Check, Clock3, FileCheck2, FilePlus2,
  FileText, FolderOpen, HardDriveUpload, MoreHorizontal, RefreshCw,
  Search, ShieldCheck, Sparkles, UploadCloud, X,
} from "lucide-react";
import SectionHeading from "../components/shared/SectionHeading";
import StatePanel from "../components/shared/StatePanel";
import StatusBadge from "../components/shared/StatusBadge";
import { isDemoMode } from "../services/api";
import { listDocuments, uploadDocument } from "../services/rolllens";
import type { RollDocument } from "../types";

type LoadState = "loading" | "ready" | "error";

function formatDate(value: string) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "Recently";
  return new Intl.DateTimeFormat("en-IN", { day: "2-digit", month: "short", year: "numeric" }).format(date);
}

function formatCount(value: number) {
  return new Intl.NumberFormat("en-IN").format(value);
}

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<RollDocument[]>([]);
  const [loadState, setLoadState] = useState<LoadState>("loading");
  const [loadError, setLoadError] = useState("");
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState<"ALL" | "READY" | "NEEDS_ATTENTION" | "PROCESSING">("ALL");
  const [uploadBusy, setUploadBusy] = useState(false);
  const [uploadMessage, setUploadMessage] = useState("");
  const [uploadError, setUploadError] = useState("");
  const [dragActive, setDragActive] = useState(false);
  const fileInput = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();
  const demo = isDemoMode();

  async function refreshDocuments() {
    setLoadState("loading");
    setLoadError("");
    try {
      const items = await listDocuments();
      setDocuments(items);
      setLoadState("ready");
    } catch (error) {
      setLoadError(error instanceof Error ? error.message : "Unable to load documents.");
      setLoadState("error");
    }
  }

  useEffect(() => {
    void refreshDocuments();
  }, []);

  const filteredDocuments = useMemo(() => {
    const normalized = search.trim().toLowerCase();
    return documents.filter((doc) => {
      const matchesSearch = !normalized || [doc.name, doc.constituency, doc.versionLabel, doc.id]
        .some((value) => value.toLowerCase().includes(normalized));
      const matchesFilter = filter === "ALL" || doc.status === filter;
      return matchesSearch && matchesFilter;
    });
  }, [documents, search, filter]);

  const totalPages = documents.reduce((sum, doc) => sum + doc.pageCount, 0);
  const readyCount = documents.filter((doc) => doc.status === "READY").length;
  const reviewCount = documents.filter((doc) => doc.status === "NEEDS_ATTENTION" || doc.status === "FAILED").length;

  async function handleFiles(fileList: FileList | null) {
    if (!fileList?.length) return;
    const file = fileList[0];
    setUploadError("");
    setUploadMessage("");
    if (!file.name.toLowerCase().endsWith(".pdf") || file.type && file.type !== "application/pdf") {
      setUploadError("Choose a PDF file. Other file types are not supported.");
      if (fileInput.current) fileInput.current.value = "";
      return;
    }
    if (file.size > 50 * 1024 * 1024) {
      setUploadError("This file is larger than the 50 MB demo limit.");
      if (fileInput.current) fileInput.current.value = "";
      return;
    }
    setUploadBusy(true);
    try {
      const created = await uploadDocument(file);
      setDocuments((current) => [created, ...current.filter((item) => item.id !== created.id)]);
      setUploadMessage(demo
        ? `${file.name} was added as a simulated demo upload. It was not sent to a backend or processed.`
        : `${file.name} was submitted successfully.`);
    } catch (error) {
      setUploadError(error instanceof Error ? error.message : "Upload failed. Please try again.");
    } finally {
      setUploadBusy(false);
      if (fileInput.current) fileInput.current.value = "";
    }
  }

  return (
    <div className="documents-page">
      <SectionHeading
        eyebrow="WORKSPACE / DOCUMENT LIBRARY"
        title="Documents"
        description="Bring electoral-roll documents into one traceable research workspace."
        actions={
          <button className="button button-primary" onClick={() => fileInput.current?.click()} disabled={uploadBusy}>
            <FilePlus2 size={17} /> {uploadBusy ? "Adding file…" : "Add document"}
          </button>
        }
      />

      <input
        ref={fileInput}
        className="visually-hidden"
        type="file"
        accept="application/pdf,.pdf"
        aria-label="Choose a PDF document"
        onChange={(event) => void handleFiles(event.target.files)}
      />

      <section className="welcome-strip">
        <div className="welcome-mark"><FolderOpen size={22} /></div>
        <div className="welcome-copy">
          <div className="welcome-title">
            <span>Research library</span>
            <span className="sample-label"><Sparkles size={12} /> {demo ? "SAMPLE WORKSPACE" : "CONNECTED API"}</span>
          </div>
          <p>{demo
            ? "Explore seeded synthetic records, preview the workflow, and test simulated uploads without live AI credentials."
            : "Documents are listed from the connected RollLens API. Processing capabilities depend on backend configuration."}</p>
        </div>
        <div className="welcome-mark-right"><ShieldCheck size={22} /></div>
      </section>

      {uploadMessage && (
        <div className="inline-notice notice-success" role="status">
          <Check size={17} /><span>{uploadMessage}</span>
          <button className="icon-button" aria-label="Dismiss message" onClick={() => setUploadMessage("")}><X size={16} /></button>
        </div>
      )}
      {uploadError && (
        <div className="inline-notice notice-error" role="alert">
          <X size={17} /><span>{uploadError}</span>
          <button className="icon-button" aria-label="Dismiss error" onClick={() => setUploadError("")}><X size={16} /></button>
        </div>
      )}

      <section className="metric-grid" aria-label="Document library summary">
        <div className="metric-card">
          <div className="metric-top"><span className="metric-icon metric-ink"><FileText size={17} /></span><span className="metric-label">DOCUMENTS</span></div>
          <div className="metric-value">{loadState === "ready" ? formatCount(documents.length) : "—"}</div>
          <div className="metric-foot">In this workspace</div>
        </div>
        <div className="metric-card">
          <div className="metric-top"><span className="metric-icon metric-teal"><FileCheck2 size={17} /></span><span className="metric-label">READY TO EXPLORE</span></div>
          <div className="metric-value">{loadState === "ready" ? formatCount(readyCount) : "—"}</div>
          <div className="metric-foot">Documents marked ready</div>
        </div>
        <div className="metric-card">
          <div className="metric-top"><span className="metric-icon metric-amber"><Clock3 size={17} /></span><span className="metric-label">NEEDS ATTENTION</span></div>
          <div className="metric-value">{loadState === "ready" ? formatCount(reviewCount) : "—"}</div>
          <div className="metric-foot">Review or retry recommended</div>
        </div>
        <div className="metric-card">
          <div className="metric-top"><span className="metric-icon metric-blue"><FileText size={17} /></span><span className="metric-label">TOTAL PAGES</span></div>
          <div className="metric-value">{loadState === "ready" ? formatCount(totalPages) : "—"}</div>
          <div className="metric-foot">Across listed documents</div>
        </div>
      </section>

      <section
        className={`upload-panel${dragActive ? " drag-active" : ""}${uploadBusy ? " upload-busy" : ""}`}
        onDragOver={(event) => { event.preventDefault(); setDragActive(true); }}
        onDragLeave={(event) => { if (!event.currentTarget.contains(event.relatedTarget as Node | null)) setDragActive(false); }}
        onDrop={(event) => { event.preventDefault(); setDragActive(false); void handleFiles(event.dataTransfer.files); }}
        aria-label="PDF upload area"
      >
        <div className="upload-symbol"><UploadCloud size={23} /></div>
        <div className="upload-copy">
          <strong>{uploadBusy ? "Adding document…" : "Add a PDF to your library"}</strong>
          <p>Drag a file here, or <button className="text-button" onClick={() => fileInput.current?.click()} disabled={uploadBusy}>browse files</button></p>
          <span>PDF only · Up to 50 MB · {demo ? "Demo uploads are simulated" : "Submitted to the connected API"}</span>
        </div>
        <button className="button button-secondary upload-choose" onClick={() => fileInput.current?.click()} disabled={uploadBusy}>
          <HardDriveUpload size={16} /> Choose PDF
        </button>
      </section>

      <section className="library-section">
        <div className="library-heading">
          <div>
            <div className="section-title-line"><h2>Your documents</h2><span className="count-chip">{documents.length}</span></div>
            <p>Manage sources before exploring extracted information.</p>
          </div>
          <button className="button button-quiet" onClick={() => void refreshDocuments()} disabled={loadState === "loading"}>
            <RefreshCw size={15} className={loadState === "loading" ? "spin" : ""} /> Refresh
          </button>
        </div>

        <div className="library-toolbar">
          <label className="search-field">
            <Search size={17} />
            <input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search documents, versions, or constituency…" aria-label="Search documents" />
            {search && <button className="search-clear" onClick={() => setSearch("")} aria-label="Clear search"><X size={14} /></button>}
          </label>
          <div className="filter-tabs" aria-label="Filter documents">
            {([
              ["ALL", "All"],
              ["READY", "Ready"],
              ["NEEDS_ATTENTION", "Needs review"],
              ["PROCESSING", "Processing"],
            ] as const).map(([value, label]) => (
              <button key={value} className={`filter-tab${filter === value ? " selected" : ""}`} onClick={() => setFilter(value)} aria-pressed={filter === value}>{label}</button>
            ))}
          </div>
        </div>

        {loadState === "loading" && <StatePanel kind="loading" title="Loading your library" description="Retrieving document metadata…" />}
        {loadState === "error" && <StatePanel kind="error" title="Documents could not be loaded" description={loadError} action={<button className="button button-secondary" onClick={() => void refreshDocuments()}><RefreshCw size={15} /> Try again</button>} />}
        {loadState === "ready" && filteredDocuments.length === 0 && (
          <StatePanel kind="empty" title={documents.length === 0 ? "Your library is empty" : "No matching documents"} description={documents.length === 0 ? "Add a PDF to get started, or use sample mode to explore the interface." : "Try a different search term or clear the selected filters."} action={documents.length > 0 ? <button className="button button-secondary" onClick={() => { setSearch(""); setFilter("ALL"); }}>Clear filters</button> : <button className="button button-primary" onClick={() => fileInput.current?.click()}><FilePlus2 size={16} /> Add a PDF</button>} />
        )}

        {loadState === "ready" && filteredDocuments.length > 0 && (
          <div className="document-list">
            {filteredDocuments.map((doc) => (
              <article className="document-row" key={doc.id}>
                <div className={`document-file-icon ${doc.origin === "SAMPLE" ? "file-sample" : "file-upload"}`}>
                  <FileText size={22} />
                  {doc.origin === "SAMPLE" && <span className="file-sparkle"><Sparkles size={10} /></span>}
                </div>
                <div className="document-main">
                  <div className="document-title-line">
                    <h3>{doc.name}</h3>
                    {doc.origin === "SAMPLE" && <span className="tiny-sample-tag">SAMPLE</span>}
                  </div>
                  <p className="document-subtitle">{doc.constituency} <span className="metadata-dot">·</span> {doc.versionLabel}</p>
                  <div className="document-meta">
                    <span><FileText size={13} /> {formatCount(doc.pageCount)} pages</span>
                    <span><span className="metadata-dot">·</span></span>
                    <span>{formatCount(doc.recordCount)} records</span>
                    <span><span className="metadata-dot">·</span></span>
                    <span>Updated {formatDate(doc.updatedAt)}</span>
                  </div>
                  {doc.status === "PROCESSING" && (
                    <div className="progress-wrap" aria-label={`${doc.processedPages} of ${doc.pageCount} pages processed`}>
                      <div className="progress-label"><span>Processing pages</span><span>{doc.processedPages}/{doc.pageCount}</span></div>
                      <div className="progress-track"><span style={{ width: `${doc.pageCount ? Math.min(100, (doc.processedPages / doc.pageCount) * 100) : 0}%` }} /></div>
                    </div>
                  )}
                  {doc.note && <p className="document-note">{doc.note}</p>}
                </div>
                <div className="document-status"><StatusBadge status={doc.status} /></div>
                <div className="document-actions">
                  <button className="button button-row-action" onClick={() => navigate(`/explore?document=${encodeURIComponent(doc.id)}`)} disabled={doc.status !== "READY"} title={doc.status === "READY" ? "Explore document" : "Document is not ready yet"}>
                    Open <ArrowRight size={15} />
                  </button>
                  <button className="icon-button" aria-label={`More options for ${doc.name}`} title="More options" onClick={() => setUploadMessage(doc.note || `${doc.name}: ${doc.status.toLowerCase().replace("_", " ")}.`)}>
                    <MoreHorizontal size={19} />
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>

      <section className="trust-note">
        <span><ShieldCheck size={16} /></span>
        <p><strong>Source integrity matters.</strong> A document being listed does not mean its extracted records have been verified. Check source evidence before relying on a result.</p>
        <span className="trust-note-end"><ArrowDownToLine size={15} /> Evidence-linked by design</span>
      </section>
    </div>
  );
}
