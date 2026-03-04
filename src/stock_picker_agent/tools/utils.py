import os
import requests
import json
from typing import Type, Any
from crewai.tools import tool, BaseTool
from pydantic import BaseModel, Field


@tool
def web_search(query: str, max_results: int = 5) -> str:
    """Search the web via Tavily and return a concise text summary."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("Missing TAVILY_API_KEY in .env")

    resp = requests.post(
        url="https://api.tavily.com/search",
        json={"api_key": api_key, "query": query, "max_results": max_results},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    # Tavily returns 'results' list with 'title', 'url', 'content'
    lines = []
    for r in data.get("results", [])[:max_results]:
        lines.append(f"- {r['title']}\n  {r['url']}\n  {r['content']}")
    return "\n".join(lines) or "No results."


# A small passthrough JSON tool so the LLM can call "json" when the
# provider validates tool calls (e.g., Groq/Grok). This accepts an
# optional `companies` list and returns a JSON string.
class JsonArgs(BaseModel):
    companies: Any = Field(None, description="Arbitrary companies data")


class JsonTool(BaseTool):
    name: str = "json"
    description: str = (
        "A simple tool that returns provided data as a JSON string."
    )
    args_schema: Type[BaseModel] = JsonArgs

    def _run(self, companies: Any = None) -> str:
        return json.dumps({"companies": companies}, ensure_ascii=False)



# Example of a custom tool to send push notifications to the user using Pushover
class PushNotification(BaseModel):
    """A message to be sent to the user"""
    message: str = Field(..., description="The message to be sent to the user.")

class PushNotificationTool(BaseTool):
    
    name: str = "Send a Push Notification"
    description: str = (
        "This tool is used to send a push notification to the user."
    )
    args_schema: Type[BaseModel] = PushNotification

    def _run(self, message: str) -> str:
        pushover_user = os.getenv("PUSHOVER_USER")
        pushover_token = os.getenv("PUSHOVER_TOKEN")
        pushover_url = "https://api.pushover.net/1/messages.json"

        print(f"Push: {message}")
        payload = {"user": pushover_user, "token": pushover_token, "message": message}
        requests.post(pushover_url, data=payload)
        return '{"notification": "ok"}'
