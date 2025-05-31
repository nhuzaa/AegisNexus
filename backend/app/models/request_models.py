from pydantic import BaseModel

class SRERequest(BaseModel):
    question: str

class SEREResponse(BaseModel):
    answer: str
    source: str