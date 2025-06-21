import os
from dotenv import load_dotenv

load_dotenv()

LOKI_URL = os.getenv("LOKI_URL", "http://localhost:3100")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
