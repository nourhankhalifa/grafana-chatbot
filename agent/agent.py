from fastapi import FastAPI, Request
import os
import requests
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time
import re

load_dotenv()

LOKI_URL = os.getenv("LOKI_URL")

app = FastAPI()

# Initialize OpenAI model
llm = ChatOpenAI(
    model="gpt-4o",  # or use "gpt-4", "gpt-3.5-turbo", etc.
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")  # Optional if it's set in the environment
)

def convert_to_shell_command(natural_language: str) -> str:
    """Uses OpenAI to convert natural language into a logQL query."""
    prompt = f"""
    Convert the following natural language request into a valid logQL query.
    Return ONLY the logQL query without any explanations.

    Examples:

    - Input: "Get all logs for service named monitoring-log-generator-1"
    - Output: {{service_name="monitoring-log-generator-1"}}

    - Input: "Show all logs for platform docker"
    - Output: {{platform="docker"}}

    - Input: "Get logs for app payment-api"
    - Output: {{app="payment-api"}}

    - Input: "Show logs from the dev namespace"
    - Output: {{namespace="dev"}}

    - Input: "Give me logs for pod auth-service-57f4dcf66b-xyz"
    - Output: {{pod="auth-service-57f4dcf66b-xyz"}}

    - Input: "I want to see logs from container nginx"
    - Output: {{container="nginx"}}

    - Input: "Get logs from node ip-192-168-1-100.ec2.internal"
    - Output: {{node="ip-192-168-1-100.ec2.internal"}}

    Only return the LogQL label selector or filter. Do NOT include time ranges or special variables like $__range.

    Now convert this request: "{natural_language}"
    """

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()

# Enable CORS for local Grafana development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def strip_time_phrase(prompt: str) -> str:
    return re.sub(r'\b(last|past|previous)\s+\d+\s+(second|seconds|minute|minutes|hour|hours|day|days)', '', prompt, flags=re.IGNORECASE).strip()


def extract_time_range(prompt: str, default_seconds: int = 300):
    # Match phrases like "last 5 minutes", "past 2 hours", etc.
    match = re.search(r'\b(last|past|previous)\s+(\d+)\s+(second|seconds|minute|minutes|hour|hours|day|days)', prompt, re.IGNORECASE)
    
    if not match:
        return default_seconds

    value = int(match.group(2))
    unit = match.group(3).lower()

    if "second" in unit:
        return value
    elif "minute" in unit:
        return value * 60
    elif "hour" in unit:
        return value * 3600
    elif "day" in unit:
        return value * 86400
    else:
        return default_seconds


@app.post("/query")
async def query_from_prompt(request: Request):
    body = await request.json()
    prompt = body.get("prompt")
    if not prompt:
        return {"error": "Missing prompt"}

    time_range_seconds = extract_time_range(prompt)
    cleaned_prompt = strip_time_phrase(prompt)
    logql = convert_to_shell_command(cleaned_prompt)

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

    loki_url = f"{LOKI_URL}/loki/api/v1/query_range"
    loki_response = requests.get(loki_url, params=params)

    if loki_response.status_code != 200:
        return {"error": "Loki query failed", "logql": logql, "details": loki_response.text}

    data = loki_response.json()
    # return {"logql": logql, "result": data}
    return {
        "logql": logql,
        "message": [
            {
                "text": stream["values"]
            }
            for stream in data.get("data", {}).get("result", [])
        ]
    }