import { BookOpenCheck } from "lucide-react";
import SectionHeading from "../components/shared/SectionHeading";
import StatePanel from "../components/shared/StatePanel";

export default function ReviewPage() {
  return (
    <div className="placeholder-page">
      <SectionHeading eyebrow="WORKSPACE / REVIEW" title="Review queue" description="Inspect uncertain fields and keep a clear history of human corrections." />
      <div className="info-callout"><BookOpenCheck size={18} /><span>Model confidence and human verification are separate signals. A field is not verified simply because an AI returned a value.</span></div>
      <StatePanel kind="empty" title="Review workflow handoff point" description="The review queue is reserved for the shared review API and the evidence viewer. Member 2 and Member 3 can integrate this module against the agreed contracts." />
    </div>
  );
}
