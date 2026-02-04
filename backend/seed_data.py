import pandas as pd
import re
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
import sys
import os

# Paths
APP_GUIDE_PATH = r"C:\Users\gsakhare\OneDrive - KC OVERSEAS EDUCATION PVT LTD\UK - Application Guide Update\Application Guide Update Schema\Application Guide Update Sheet.xlsx"
COURSE_SHEET_PATH = r"C:\Users\gsakhare\OneDrive - KC OVERSEAS EDUCATION PVT LTD\UK - Consolidated Sheets\Consolidated Sheet 15 Jan 2026.xlsx"

def clean_money(val):
    if pd.isna(val):
        return 0.0
    val = str(val)
    # Remove currency symbols and commas
    clean = re.sub(r'[^\d.]', '', val)
    try:
        return float(clean)
    except:
        return 0.0

def clean_gpa(row):
    # Try OutOf10 first, then OutOf4
    val = row.get('EntryRequirementUgOutOf10')
    if pd.notna(val) and val != 0:
        return float(val)
    
    val = row.get('EntryRequirementUgOutOf4')
    if pd.notna(val) and val != 0:
        # Convert 4.0 scale to raw or keep? Schema says float.
        return float(val)
    
    # Fallback/Default
    return 0.0

def seed():
    # Create tables if they don't exist
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Check connection
    if not engine:
        print("Database engine not configured. Set DATABASE_URL.")
        return

    print("Reading Excel files... this may take a moment.")
    try:
        df_courses = pd.read_excel(COURSE_SHEET_PATH)
        df_guide = pd.read_excel(APP_GUIDE_PATH, sheet_name="Application Guide Updates")
    except Exception as e:
        print(f"Error reading files: {e}")
        return

    print("Processing Universities...")
    # Extract unique universities from Course Sheet
    unique_unis = df_courses['UniversityName'].unique()
    
    uni_name_to_id = {}
    
    for uni_name in unique_unis:
        if pd.isna(uni_name):
            continue
            
        uni_name = str(uni_name).strip()
        
        # Check if exists
        existing = db.query(models.UniversityProfile).filter(models.UniversityProfile.name == uni_name).first()
        if not existing:
            new_uni = models.UniversityProfile(
                name=uni_name,
                country="UK", # Default per requirement
                # logic for logo_url could go here if available
            )
            db.add(new_uni)
            db.commit()
            db.refresh(new_uni)
            uni_name_to_id[uni_name] = new_uni.uni_id
        else:
            uni_name_to_id[uni_name] = existing.uni_id

    print(f"Synced {len(uni_name_to_id)} universities.")

    print("Processing Courses...")
    # Bulk insert might be faster, but let's do row by row for safety/validation first or chunks
    courses_to_add = []
    
    # Limit to first 2000 for safety if file is huge? or all.
    # df_courses = df_courses.head(2000) 
    
    for index, row in df_courses.iterrows():
        uni_name = str(row.get('UniversityName')).strip()
        uni_id = uni_name_to_id.get(uni_name)
        
        if not uni_id:
            continue

        try:
            tuition = clean_money(row.get('Amount'))
            gpa = clean_gpa(row)
            ielts = float(row.get('IeltsOverall', 0.0)) if pd.notna(row.get('IeltsOverall')) else 0.0
            
            course = models.CourseCatalog(
                uni_id=uni_id,
                course_name=str(row.get('CourseName', 'Unknown')),
                level_code=str(row.get('StudyLevelId', '')), # Check if this maps to UG/PG
                intake_months=str(row.get('Intakes', '')),
                tuition_fee=tuition,
                is_stem=bool(row.get('IsStemCourse', False)),
                has_internship=bool(row.get('InternshipAvailable', False)),
                min_ielts_overall=ielts,
                min_gpa_ug=gpa,
                backlog_limit=int(row.get('backlog', 0)) if pd.notna(row.get('backlog')) and str(row.get('backlog')).isdigit() else 0,
                is_moi_accepted=bool(row.get('IsMOIWaiver', False))
            )
            courses_to_add.append(course)
        except Exception as e:
            print(f"Skipping course row {index}: {e}")
            continue

        if len(courses_to_add) >= 500:
            db.bulk_save_objects(courses_to_add)
            db.commit()
            courses_to_add = []
            
    if courses_to_add:
        db.bulk_save_objects(courses_to_add)
        db.commit()

    print("Processing Operational Procedures...")
    procs_to_add = []
    
    # Filter for needed columns in guide
    # 'University Name', 'Information - Category', 'Information - Sub Category', 'Description - KC Team'
    for index, row in df_guide.iterrows():
        uni_name = str(row.get('University Name')).strip()
        
        # Try to find ID. Note: Guide might have slightly different names.
        # Simple match for now.
        uni_id = uni_name_to_id.get(uni_name)
        
        if not uni_id:
            # Maybe log fuzzy match failure?
            continue
            
        category = str(row.get('Information - Category', ''))
        sub_cat = str(row.get('Information - Sub Category', ''))
        full_cat = f"{category} - {sub_cat}" if sub_cat else category
        
        content = str(row.get('Description - KC Team', ''))
        
        proc = models.OperationalProcedure(
            uni_id=uni_id,
            category=full_cat,
            content=content
        )
        procs_to_add.append(proc)
        
        if len(procs_to_add) >= 500:
            db.bulk_save_objects(procs_to_add)
            db.commit()
            procs_to_add = []

    if procs_to_add:
        db.bulk_save_objects(procs_to_add)
        db.commit()

    print("Seed complete.")
    db.close()

if __name__ == "__main__":
    seed()
