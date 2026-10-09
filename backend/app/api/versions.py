from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field
from app.services.comparison import compare_records
router = APIRouter()
class CompareRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    old_version_id: str
    new_version_id: str
    old_records: list[dict] = Field(max_length=10000)
    new_records: list[dict] = Field(max_length=10000)
class CompareResponse(BaseModel):
    old_version_id: str
    new_version_id: str
    changes: list[dict]
    caveats: list[str]
@router.post("/versions/compare", response_model=CompareResponse)
def compare_versions(request: CompareRequest):
    return CompareResponse(old_version_id=request.old_version_id,new_version_id=request.new_version_id,
      changes=compare_records(request.old_records,request.new_records),caveats=["Matches are candidates, not proof that two records represent the same person.","Review every change against source pages before drawing conclusions.","Aggregate anomalies must never be interpreted as proof of wrongdoing."])
