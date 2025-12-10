from typing import Dict

from fastapi import APIRouter
from fastapi.responses import FileResponse

from src.pdf.generate import GeneratePDF
from .models import RequesterData, ResponseData

router = APIRouter(prefix='/generating')


@router.post("")
async def generate_report(payload: Dict):
    requester = RequesterData(**payload['requester'])
    reponse = ResponseData(**payload['response'])
    pdf = GeneratePDF(requester, reponse).generate()
    return FileResponse(f"/app/{pdf}")
