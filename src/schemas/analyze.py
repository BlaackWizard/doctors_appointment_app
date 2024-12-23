from fastapi import UploadFile
from pydantic import BaseModel


class SAnalyzeRequest(BaseModel):
    analyze_name: str
    result: str
    file: UploadFile
    medical_card_id: int
