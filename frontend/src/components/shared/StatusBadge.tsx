import type { DocumentStatus } from "../../types";

const labels: Record<DocumentStatus, string> = {
  READY: "Ready",
  PROCESSING: "Processing",
  NEEDS_ATTENTION: "Needs review",
  FAILED: "Failed",
};

export default function StatusBadge({ status }: { status: DocumentStatus }) {
  return <span className={`status-badge status-${status.toLowerCase().replace("_", "-")}`}>
    <span className="badge-dot" />{labels[status]}
  </span>;
}
