from fastapi import APIRouter, Request, HTTPException
from agent.models.request import PromptRequest
from agent.services.logql import query_loki
from agent.services.summarizer import get_summary, is_summary_request

router = APIRouter()

@router.post("/query")
async def handle_query(request: Request):
    body = await request.json()
    prompt = body.get("prompt")
    if not prompt:
        raise HTTPException(status_code=400, detail="Missing prompt")

    try:
        result = await query_loki(prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
