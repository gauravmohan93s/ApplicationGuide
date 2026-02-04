from typing import List, Optional
from pydantic import BaseModel
from decimal import Decimal

class OperationalProcedureBase(BaseModel):
    category: str
    content: Optional[str] = None

class OperationalProcedure(OperationalProcedureBase):
    proc_id: int
    uni_id: int
    class Config:
        orm_mode = True

class ScholarshipBase(BaseModel):
    title: str
    max_amount: Optional[int] = None
    description: Optional[str] = None

class Scholarship(ScholarshipBase):
    schol_id: int
    uni_id: int
    class Config:
        orm_mode = True

class UniversityBase(BaseModel):
    name: str
    country: str
    logo_url: Optional[str] = None
    is_high_risk_region_accepted: bool

class University(UniversityBase):
    uni_id: int
    class Config:
        orm_mode = True

class CourseBase(BaseModel):
    course_name: str
    level_code: Optional[str]
    intake_months: Optional[str]
    tuition_fee: Optional[Decimal]
    is_stem: bool
    has_internship: bool
    min_ielts_overall: Optional[float]
    min_gpa_ug: Optional[float]
    backlog_limit: Optional[int]
    is_moi_accepted: bool

class Course(CourseBase):
    course_id: int
    uni_id: int
    university: Optional[University] = None
    class Config:
        orm_mode = True

class UniversityFactsheet(University):
    procedures: List[OperationalProcedure] = []
    scholarships: List[Scholarship] = []
