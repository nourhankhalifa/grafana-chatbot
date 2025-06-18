from fastapi import FastAPI, Request
import os
import requests
import re
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage
from fastapi.middleware.cors import CORSMiddleware

LOKI_URL = os.getenv("LOKI_URL")

app = FastAPI()

llm = ChatOllama(model="llama3.2", base_url="http://host.docker.internal:11434")

def convert_to_shell_command(natural_language: str) -> str:
    """Uses Ollama's LLM to convert natural language input into a logQL queries."""
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

    Now convert this request: "{natural_language}"
    """

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()  # Extract command from LLM response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Grafana URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query")
async def query_from_prompt(request: Request):
    body = await request.json()
    prompt = body.get("prompt")
    if not prompt:
        return {"error": "Missing prompt"}

    # logql = extract_logql(generate_logql_with_ollama(prompt))
    logql = convert_to_shell_command(prompt)
    print(logql)
    params = {"query": logql}
    
    loki_url = f"{LOKI_URL}/loki/api/v1/query"

    # Send the GET request with query encoded
    loki_response = requests.get(loki_url, params=params)

    if loki_response.status_code != 200:
        return {"error": "Loki query failed", "logql": logql, "details": loki_response.text}

    data = loki_response.json()
    print(data)
    # return {"logql": logql, "message": data}
    return {
        "logql": logql,
        "message": [
            {
                "text": stream["values"]
            }
            for stream in data.get("data", {}).get("result", [])
        ]
    }
