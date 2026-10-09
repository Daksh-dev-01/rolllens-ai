from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.safe_query import plan_question, execute_plan
router = APIRouter()
class QueryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question: str = Field(min_length=1, max_length=1000)
    document_id: str | None = None
    version_id: str | None = None
class QueryResponse(BaseModel):
    answer: str
    scope: dict
    result_table: list[dict]
    caveats: list[str]
@router.post("/queries", response_model=QueryResponse)
def query_records(request: QueryRequest, db: Session = Depends(get_db)):
    try: plan = plan_question(request.question, request.document_id, request.version_id)
    except ValueError as e: raise HTTPException(status_code=422, detail=str(e))
    try: rows = execute_plan(db, plan)
    except Exception as e:
        # Avoid returning SQL/DB internals to callers.
        raise HTTPException(status_code=503, detail="Query service unavailable; verify database schema and connectivity") from e
    if plan.kind == "record_count": answer = f"{rows[0]['record_count']} records are in the selected scope." if rows else "No records found in the selected scope."
    elif plan.kind == "unverified_count": answer = f"{rows[0]['unverified_count']} records are not marked human-verified." if rows else "No records found in the selected scope."
    else: answer = "Age-group distribution calculated for the selected scope."
    return QueryResponse(answer=answer, scope={"document_id":plan.document_id,"version_id":plan.version_id}, result_table=rows,
      caveats=["Aggregate statistics only; no individual-level records are returned.","Extraction confidence is not equivalent to human verification.","Anomalies are indicators for review, not evidence of wrongdoing."])
