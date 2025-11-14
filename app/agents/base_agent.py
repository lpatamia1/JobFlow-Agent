# app/agents/base_agent.py
from typing import Any, Dict

class BaseAgent:
    name: str = "base-agent"

    def run(self, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError
