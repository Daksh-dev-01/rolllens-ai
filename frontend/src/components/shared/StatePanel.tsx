import type { ReactNode } from "react";
import { AlertCircle, CheckCircle2, FileSearch, LoaderCircle } from "lucide-react";

type StateKind = "loading" | "empty" | "error" | "success";

const icons = {
  loading: LoaderCircle,
  empty: FileSearch,
  error: AlertCircle,
  success: CheckCircle2,
};

export default function StatePanel({
  kind,
  title,
  description,
  action,
}: {
  kind: StateKind;
  title: string;
  description: string;
  action?: ReactNode;
}) {
  const Icon = icons[kind];
  return (
    <div className={`state-panel state-${kind}`} role={kind === "error" ? "alert" : "status"}>
      <span className="state-icon"><Icon size={21} className={kind === "loading" ? "spin" : ""} /></span>
      <div className="state-copy">
        <strong>{title}</strong>
        <p>{description}</p>
        {action && <div className="state-action">{action}</div>}
      </div>
    </div>
  );
}
