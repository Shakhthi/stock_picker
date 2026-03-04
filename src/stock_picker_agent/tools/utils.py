import os
import requests
import json
from crewai.tools import tool


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



@tool("json")
def json_output(companies: list) -> str:
    """Returns structured JSON output of companies."""
    return json.dumps({"companies": companies}, indent=2)
