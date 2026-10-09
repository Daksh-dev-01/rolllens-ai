"""Constrained aggregate query planner. Never executes model-generated SQL."""
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class QueryPlan:
    kind: str
    document_id: str | None = None
    version_id: str | None = None
    age_min: int | None = None
    age_max: int | None = None

ALLOWED_KINDS = {"record_count", "age_distribution", "unverified_count"}

def plan_question(question: str, document_id: str | None = None, version_id: str | None = None) -> QueryPlan:
    q = " ".join(question.lower().strip().split())
    if not q or len(q) > 1000: raise ValueError("question is empty or too long")
    individual_terms = ("show names", "list voters", "voter id", "phone number", "address of")
    if any(term in q for term in individual_terms): raise ValueError("individual-level personal data is not available through aggregate queries")
    if any(x in q for x in ("delete ", "update ", "insert ", "drop ", "alter ", "truncate ", ";", "--", "/*")):
        raise ValueError("unsupported or unsafe question")
    if any(k in q for k in ("unverified", "not verified", "needs review", "uncertain field")): kind = "unverified_count"
    elif "age" in q and any(k in q for k in ("distribution", "group", "breakdown", "range")): kind = "age_distribution"
    elif any(k in q for k in ("how many", "count", "number of", "records present", "total records")) and any(k in q for k in ("record", "voter", "document", "dataset", "present", "total")): kind = "record_count"
    else: raise ValueError("unsupported question; try record count, age-group distribution, or unverified-field count")
    return QueryPlan(kind, document_id, version_id)

FILTER = "(:document_id IS NULL OR dv.document_id = :document_id) AND (:version_id IS NULL OR dv.id = :version_id)"
SQL = {
 "record_count": f"SELECT COUNT(*) AS record_count FROM records r JOIN pages p ON p.id = r.page_id JOIN document_versions dv ON dv.id = p.document_version_id WHERE {FILTER}",
 "unverified_count": f"SELECT COUNT(*) AS unverified_count FROM records r JOIN pages p ON p.id = r.page_id JOIN document_versions dv ON dv.id = p.document_version_id WHERE r.verification_status <> 'verified' AND {FILTER}",
 "age_distribution": f"SELECT CASE WHEN r.age < 18 THEN 'under 18' WHEN r.age BETWEEN 18 AND 29 THEN '18-29' WHEN r.age BETWEEN 30 AND 44 THEN '30-44' WHEN r.age BETWEEN 45 AND 59 THEN '45-59' WHEN r.age >= 60 THEN '60+' ELSE 'unknown' END AS age_group, COUNT(*) AS record_count FROM records r JOIN pages p ON p.id = r.page_id JOIN document_versions dv ON dv.id = p.document_version_id WHERE {FILTER} GROUP BY age_group ORDER BY age_group LIMIT 20"
}

def execute_plan(session: Any, plan: QueryPlan, timeout_ms: int = 3000, limit: int = 100):
    if plan.kind not in ALLOWED_KINDS: raise ValueError("query plan not approved")
    if not 100 <= timeout_ms <= 10000: raise ValueError("invalid timeout")
    if not 1 <= limit <= 100: raise ValueError("invalid result limit")
    from sqlalchemy import text
    bind = getattr(session, "bind", None)
    if bind is not None and bind.dialect.name == "postgresql":
        session.execute(text("SELECT set_config('statement_timeout', :timeout, true)"), {"timeout": str(timeout_ms)})
    result = session.execute(text(SQL[plan.kind]), {"document_id": plan.document_id, "version_id": plan.version_id})
    return [dict(row) for row in result.mappings().fetchmany(limit)]
