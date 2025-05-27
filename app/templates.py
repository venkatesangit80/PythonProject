from app.agents.support import help as help_agent
from app.agents.capacity_management import server_health

TEMPLATES = [
    {
        "id": "welcome_health_check",
        "name": "Welcome + Server Health",
        "description": "Greets the user and checks server health.",
        "parameters": [
            {"name": "name", "label": "User Name", "type": "string"}
        ],
        "agents": [help_agent, server_health]
    }
]