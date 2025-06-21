import re

def extract_time_range(prompt: str, default_seconds: int = 300):
    match = re.search(r'\b(last|past|previous)\s+(\d+)\s+(second|minute|hour|day)s?', prompt, re.IGNORECASE)
    if not match:
        return default_seconds

    value = int(match.group(2))
    unit = match.group(3).lower()

    return {
        "second": value,
        "minute": value * 60,
        "hour": value * 3600,
        "day": value * 86400
    }.get(unit, default_seconds)

def strip_time_phrase(prompt: str) -> str:
    return re.sub(r'\b(last|past|previous)\s+\d+\s+(second|seconds|minute|minutes|hour|hours|day|days)', '', prompt, flags=re.IGNORECASE).strip()
