# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import agent modules
from app.agents import capacity_management, support
from app.filters import content_check

# Initialize FastAPI app
app = FastAPI(title="Agentic Chatbot Backend")

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class MessageIn(BaseModel):
    message: str

class MessageOut(BaseModel):
    response: str
    agent: str

# Agent registry (factory style)
AGENT_MAP = {
    "server health": capacity_management.server_health,
    "help": support.help,
}

DEFAULT_AGENT = support.default_response

@app.post("/chat", response_model=MessageOut)
async def chat_endpoint(msg: MessageIn):
    user_msg = msg.message.strip()
    user_msg_lower = user_msg.lower()

    # Step 1: Content filtering
    if content_check.contains_profanity(user_msg):
        return {
            "response": "⚠️ Inappropriate language detected. Please use respectful language.",
            "agent": "moderation"
        }
    if content_check.is_spam(user_msg):
        return {
            "response": "⚠️ Your message was flagged as spam. Please rephrase it.",
            "agent": "moderation"
        }

    # Step 2: Agent routing (based on trigger word in message)
    chosen_trigger = None
    for trigger in AGENT_MAP:
        if trigger in user_msg_lower:
            chosen_trigger = trigger
            break

    # Step 3: Execute agent
    agent_func = AGENT_MAP.get(chosen_trigger, DEFAULT_AGENT)
    response_text = agent_func(user_msg)
    resolved_agent = chosen_trigger if chosen_trigger else "default"

    return {
        "response": response_text,
        "agent": resolved_agent
    }