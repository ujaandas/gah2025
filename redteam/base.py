from enum import Enum
import requests
from typing import Dict, Any

BASE_URL = "https://6ofr2p56t1.execute-api.us-east-1.amazonaws.com/prod"


class Target(Enum):
    ELEPHANT = "/api/elephant"
    FOX = "/api/fox"
    EAGLE = "/api/eagle"
    ANT = "/api/ant"
    WOLF = "/api/wolf"
    BEAR = "/api/bear"
    CHAMELEON = "/api/chameleon"


def message_target(target: Target, msg: str) -> Dict[str, Any]:
    url = BASE_URL + target.value
    payload = {"message": msg}

    try:
        response = requests.post(url, json=payload, timeout=35)
    except requests.exceptions.Timeout:
        return {"error": "timeout", "message": "Agent did not respond in time"}
    except requests.exceptions.RequestException as e:
        return {"error": "request_failed", "message": str(e)}

    status = response.status_code
    result: Dict[str, Any] = {}

    if status == 200:
        result = response.json()
        print(f"Response: {result.get('response', 'No response field')}")
    elif status == 503:
        result = {"error": "service_unavailable", "message": "Queue full, retry later"}
    elif status == 504:
        result = {"error": "timeout", "message": "Agent took too long to respond"}
    elif status == 500:
        result = {"error": "server_error", "message": "Internal server error"}
    else:
        result = {"error": "unexpected_status", "status": status}

    return result
