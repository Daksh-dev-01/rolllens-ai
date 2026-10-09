import { GitCompareArrows } from "lucide-react";
import SectionHeading from "../components/shared/SectionHeading";
import StatePanel from "../components/shared/StatePanel";

export default function ComparePage() {
  return (
    <div className="placeholder-page">
      <SectionHeading eyebrow="WORKSPACE / COMPARE" title="Compare versions" description="Review candidate additions, removals, and modifications across document versions." />
      <div className="info-callout"><GitCompareArrows size={18} /><span>Differences are investigation leads, not proof of an error or wrongdoing. Ambiguous matches should be reviewed by a person.</span></div>
      <StatePanel kind="empty" title="Comparison module handoff point" description="Member 4 owns the comparison logic. This page is intentionally a safe integration placeholder until the shared response contract is implemented." />
    </div>
  );
}
