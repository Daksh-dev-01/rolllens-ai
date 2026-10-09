from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models.entities import Record, Page, DocumentVersion

def aggregate(db: Session):
    base = select(Record).join(Page, Record.page_id == Page.id).join(DocumentVersion, Page.document_version_id == DocumentVersion.id).where(DocumentVersion.is_active.is_(True)).subquery()
    total = db.scalar(select(func.count()).select_from(base)) or 0
    verified = db.scalar(select(func.count()).select_from(base).where(base.c.verification_status == "verified")) or 0
    age_avg = db.scalar(select(func.avg(base.c.age)).where(base.c.age.is_not(None)))
    genders = db.execute(select(base.c.gender, func.count()).group_by(base.c.gender)).all()
    ages = db.execute(select(base.c.age).where(base.c.age.is_not(None))).scalars().all()
    bins = [("Under 18", lambda age: age < 18), ("18–29", lambda age: 18 <= age <= 29), ("30–44", lambda age: 30 <= age <= 44), ("45–59", lambda age: 45 <= age <= 59), ("60+", lambda age: age >= 60)]
    age_groups = [{"label": label, "count": sum(1 for age in ages if predicate(age))} for label, predicate in bins]
    age_groups.append({"label": "Unknown / not recorded", "count": max(0, total - len(ages))})
    gender_breakdown = {g or "Unknown / not recorded": n for g, n in genders}
    gender_distribution = [{"label": label, "count": count} for label, count in gender_breakdown.items()]
    return {"total_records": total, "verified_records": verified, "unverified_records": total - verified,
            "average_age": round(age_avg, 1) if age_avg is not None else None, "gender_breakdown": gender_breakdown,
            "age_groups": age_groups, "gender_distribution": gender_distribution,
            "dataset_name": "Active document versions", "dataset_scope": "Records belonging to active document versions"}
