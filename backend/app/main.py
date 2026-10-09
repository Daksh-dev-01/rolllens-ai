from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.config import settings
from app.db.session import Base, engine
from app.models import entities  # register ORM models before table creation
from app.api import documents, records, analytics, reviews, queries, versions

app = FastAPI(title=settings.app_name, version="1.0.0", description="Evidence-first document intelligence API")
Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    if settings.demo_mode:
        from app.db.seed import seed
        seed()

@app.exception_handler(404)
async def not_found(request: Request, exc):
    return JSONResponse(status_code=404, content={"success": False, "error": {"code": "NOT_FOUND", "message": str(getattr(exc, "detail", "Not found"))}})

@app.exception_handler(422)
async def validation_error(request: Request, exc):
    detail = getattr(exc, "detail", "Validation failed")
    return JSONResponse(status_code=422, content={"success": False, "error": {"code": "VALIDATION_ERROR", "message": detail}})

@app.get(settings.api_prefix + "/health", tags=["health"])
def health():
    return {"success": True, "data": {"status": "ok", "service": "rolllens-ai", "demo_mode": settings.demo_mode}}

app.include_router(documents.router, prefix=settings.api_prefix)
app.include_router(records.router, prefix=settings.api_prefix)
app.include_router(analytics.router, prefix=settings.api_prefix)
app.include_router(reviews.router, prefix=settings.api_prefix)
app.include_router(queries.router, prefix=settings.api_prefix)
app.include_router(versions.router, prefix=settings.api_prefix)
