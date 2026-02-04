from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Text, Decimal
from sqlalchemy.orm import relationship
from .database import Base

class UniversityProfile(Base):
    __tablename__ = "university_profiles"

    uni_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    country = Column(String, default="UK")
    logo_url = Column(String, nullable=True)
    is_high_risk_region_accepted = Column(Boolean, default=False)

    courses = relationship("CourseCatalog", back_populates="university")
    procedures = relationship("OperationalProcedure", back_populates="university")
    scholarships = relationship("Scholarship", back_populates="university")

class CourseCatalog(Base):
    __tablename__ = "course_catalog"

    course_id = Column(Integer, primary_key=True, index=True)
    uni_id = Column(Integer, ForeignKey("university_profiles.uni_id"))
    course_name = Column(String, index=True)
    level_code = Column(String) # UG/PG
    intake_months = Column(String) # Comma separated
    tuition_fee = Column(Decimal(10, 2))
    is_stem = Column(Boolean, default=False)
    has_internship = Column(Boolean, default=False)
    min_ielts_overall = Column(Float)
    min_gpa_ug = Column(Float)
    backlog_limit = Column(Integer)
    is_moi_accepted = Column(Boolean, default=False)

    university = relationship("UniversityProfile", back_populates="courses")

class OperationalProcedure(Base):
    __tablename__ = "operational_procedures"

    proc_id = Column(Integer, primary_key=True, index=True)
    uni_id = Column(Integer, ForeignKey("university_profiles.uni_id"))
    category = Column(String) # e.g., 'CAS', 'Refund'
    content = Column(Text)

    university = relationship("UniversityProfile", back_populates="procedures")

class Scholarship(Base):
    __tablename__ = "scholarships"

    schol_id = Column(Integer, primary_key=True, index=True)
    uni_id = Column(Integer, ForeignKey("university_profiles.uni_id"))
    title = Column(String)
    max_amount = Column(Integer)
    description = Column(Text)

    university = relationship("UniversityProfile", back_populates="scholarships")
