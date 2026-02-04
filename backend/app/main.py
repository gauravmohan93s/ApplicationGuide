from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import os

from . import models, schemas, database

# Create tables if they don't exist (helpful for quick start, though migration tool preferred)
if database.engine:
    models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="KC Overseas Operations Portal")

# CORS Setup
origins = [
    "http://localhost:5173", # Vite default
    os.getenv("FRONTEND_URL", "*")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stats")
def get_stats(db: Session = Depends(database.get_db)):
    uni_count = db.query(models.UniversityProfile).count()
    course_count = db.query(models.CourseCatalog).count()
    return {"status": "healthy", "universities": uni_count, "courses": course_count}

@app.get("/search", response_model=List[schemas.Course])
def search_courses(
    min_gpa: Optional[float] = Query(None),
    max_tuition: Optional[float] = Query(None),
    ielts_score: Optional[float] = Query(None),
    backlogs: Optional[int] = Query(None),
    is_stem: Optional[bool] = Query(None),
    db: Session = Depends(database.get_db)
):
    query = db.query(models.CourseCatalog).join(models.UniversityProfile)

    if min_gpa is not None:
        query = query.filter(models.CourseCatalog.min_gpa_ug <= min_gpa)
    if max_tuition is not None:
        query = query.filter(models.CourseCatalog.tuition_fee <= max_tuition)
    if ielts_score is not None:
        query = query.filter(models.CourseCatalog.min_ielts_overall <= ielts_score)
    if backlogs is not None:
        query = query.filter(models.CourseCatalog.backlog_limit >= backlogs)
    if is_stem is not None:
        query = query.filter(models.CourseCatalog.is_stem == is_stem)
    
    # Limit results for performance
    return query.limit(50).all()

@app.get("/university/{uni_id}/factsheet", response_model=schemas.UniversityFactsheet)
def get_university_factsheet(uni_id: int, db: Session = Depends(database.get_db)):
    uni = db.query(models.UniversityProfile).filter(models.UniversityProfile.uni_id == uni_id).first()
    if not uni:
        raise HTTPException(status_code=404, detail="University not found")
    return uni
