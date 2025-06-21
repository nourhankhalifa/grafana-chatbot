from agent.config import OPENAI_API_KEY
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    api_key=OPENAI_API_KEY
)

def convert_prompt_to_logql(natural_language: str) -> str:
    prompt = f"""
    Convert the following natural language request into a valid logQL query.
    Return ONLY the logQL query without any explanations.

    Examples:
    - Input: "Get logs for payment-api"
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
    return response.content.strip()

def is_summary_request(prompt: str) -> bool:
    summary_keywords = ["summarize", "what happened", "explain"]
    return any(k in prompt.lower() for k in summary_keywords)

def get_summary(log_lines: list[str]) -> str:
    logs = "\n".join(log_lines[:50])
    prompt = f"""Summarize the following logs:\n\n{logs}"""
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()
