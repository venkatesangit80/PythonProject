from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import asyncio

from app.filters import content_check
from app.agents import support, capacity_management
from app.templates import TEMPLATES

app = FastAPI(title="Guided Agentic Chatbot Backend")

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agent routing map for free chat mode
AGENT_MAP = {
    "server health": capacity_management.server_health,
    "help": support.help,
}
DEFAULT_AGENT = support.default_response

# -----------------------------
# Models for guided agentic mode
# -----------------------------

class TemplateExecutionRequest(BaseModel):
    template_id: str
    params: Dict[str, Any]

# -----------------------------
# Chat Mode: Freeform Routing
# -----------------------------

@app.post("/chat")
async def chat_fallback(message: str):
    if content_check.contains_profanity(message):
        return {
            "response": "⚠️ Inappropriate language detected. Please use respectful language.",
            "agent": "moderation"
        }
    if content_check.is_spam(message):
        return {
            "response": "⚠️ Your message was flagged as spam. Please rephrase it.",
            "agent": "moderation"
        }

    msg_lower = message.lower()
    for trigger, func in AGENT_MAP.items():
        if trigger in msg_lower:
            response = await run_agent(func, {"message": message})
            return {
                "response": response,
                "agent": trigger
            }

    response = await run_agent(DEFAULT_AGENT, {"message": message})
    return {
        "response": response,
        "agent": "default"
    }

# -----------------------------
# Guided Agentic Mode Endpoints
# -----------------------------

@app.get("/templates")
async def get_templates():
    return [
        {
            "id": t["id"],
            "name": t["name"],
            "description": t["description"],
            "parameters": t["parameters"]
        }
        for t in TEMPLATES
    ]

@app.post("/templates/execute")
async def execute_template(request: TemplateExecutionRequest):
    template = next((t for t in TEMPLATES if t["id"] == request.template_id), None)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    results = await asyncio.gather(
        *(run_agent(agent, request.params) for agent in template["agents"])
    )

    return {
        "template": template["name"],
        "parameters": request.params,
        "results": results
    }

# -----------------------------
# Utility: Run agent safely
# -----------------------------

async def run_agent(agent_func, params: dict):
    if asyncio.iscoroutinefunction(agent_func):
        return await agent_func(params)
    else:
        return agent_func(params)