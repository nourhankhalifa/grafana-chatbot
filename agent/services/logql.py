import time
import requests
from agent.config import LOKI_URL
from agent.utils.time_parsing import extract_time_range, strip_time_phrase
from agent.services.summarizer import convert_prompt_to_logql, get_summary, is_summary_request
from langchain.schema import HumanMessage

async def query_loki(prompt: str):
    time_range_seconds = extract_time_range(prompt)
    cleaned_prompt = strip_time_phrase(prompt)
    logql = convert_prompt_to_logql(cleaned_prompt)

    now = int(time.time())
    start = now - time_range_seconds
    end = now

    params = {
        "query": logql,
        "start": str(start * 1_000_000_000),
        "end": str(end * 1_000_000_000),
        "limit": 1000,
        "direction": "backward",
    }

    loki_response = requests.get(f"{LOKI_URL}/loki/api/v1/query_range", params=params)
    if loki_response.status_code != 200:
        raise Exception(f"Loki query failed: {loki_response.text}")

    data = loki_response.json()

    log_lines = []
    for stream in data.get("data", {}).get("result", []):
        for _, value in stream["values"]:
            log_lines.append(value)

    if is_summary_request(prompt) and log_lines:
        summary = get_summary(log_lines)
        return {"logql": logql, "message": summary}

    if not log_lines:
        return {"logql": logql, "message": "No log data returned."}

    return {"logql": logql, "message": [{"text": log_lines}]}
