from pydantic import BaseModel, Field
from typing import Optional

class Experiece(BaseModel):
    role: str
    company: str
    duration: str
    highlights: list[str] = Field(description="List of key achievements or responsibilities in this role")

class Education(BaseModel):
    degree: str
    institution: str
    graduation_year: int
    details: Optional[str] = Field(description="Additional details about the education, such as honors or relevant coursework")

class CVData(BaseModel):
    name: str
    email: str
    summary: Optional[str] = Field(description="A brief summary or objective statement")
    experience: list[Experiece] 
    education: list[Education] 
    skills: list[str]

class JobRequirements(BaseModel):
    title: str
    required_skills: list[str]
    nice_to_have_skills: Optional[list[str]] = Field(description="Skills that are not mandatory but would be a plus")
    min_years_experience: int
    key_responsibilities: list[str] 
    seniority_level: str = Field(description="The seniority level of the position, e.g., Junior, Mid, Senior")


class SkillMatch(BaseModel):
    skill: str
    present_in_cv: bool
    evidence: Optional[str] = None

class MatchAnalysis(BaseModel):
    overall_score: int = Field(ge=0, le=100, description="Overall match score between the CV and the job description")
    skills_score: int = Field(ge=0, le=100, description="Score based on the skills match")
    experience_score: int = Field(ge=0, le=100, description="Score based on the experience match")
    seniority_fit: str
    skill_matches: list[SkillMatch] 
    missing_critical_skills: list[str] 
    strengths: list[str]
    gaps: list[str]