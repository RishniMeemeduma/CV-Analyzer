import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from schemas import CVData, JobRequirements, MatchAnalysis
from logger import logger

load_dotenv()
key = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # required by SDK but ignored by Ollama
)
MODEL = "qwen2.5:7b"

def _call_structured(system: str, user: str, schema: type[BaseModel]) -> BaseModel:
    """Helper : call claude and parse response into pydynamic model"""

    response = client.chat.completions.parse(
        model = MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        response_format=schema,
        temperature=0.1
    )
    return response.choices[0].message.parsed

def extract_cv_data(cv_text: str) -> CVData:
    system = "You extract structured data from CVs/resumes. Be accurate and complete. Infer years_of_experience from roles"
    return _call_structured(system, cv_text, CVData)

def extract_job_requirements(job_text: str) -> JobRequirements:
    system = "You extract structured requirements from job descriptions. Distinguish must-haves from nice-to-haves"
    return _call_structured(system, job_text, JobRequirements)

def analyze_match(cv:CVData, job: JobRequirements) -> MatchAnalysis:
    system = """You aare a technical recruiter. compare a cv to a job.
    score fairly - overall_score weights skills 50%, experience 30%, seniority fit 20%.
    For each required and nice-to-have skill, check if the cv has evidence of it.
    Be specific about the gaps and strengths."""
    user = f"CV:\n{cv.model_dump_json(indent=2)}\n\nJob:\n{job.model_dump_json(indent=2)}"
    return _call_structured(system, user, MatchAnalysis)

def generate_feedback(cv:CVData, job: JobRequirements, analysis: MatchAnalysis) -> str:
    """Streaming text feedback -not structured"""
    system = """You are a career coach. Give specific, actionable feedback to help this candidate improve their CV for this role.
    Include: (1) what to emphasize more, (2) what's missing and how to address it, 
    (3) 2-3 suggested bullet-point rewrites for their experience section """
    user = f"CV: {cv.model_dump_json()}\nJob: {job.model_dump_json()}\nAnalysis: {analysis.model_dump_json()}"

    stream = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        stream=True,
        temperature=0.7,
    )
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content