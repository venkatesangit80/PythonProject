# app/agents/support.py

async def help(prompt: str) -> str:
    """
    Provides help or usage guidance to the user.
    """
    return (
        "🆘 Help Guide:\n"
        "- Ask me about the 'server health' to check system status.\n"
        "- Say 'help' to view this message again.\n\n"
        "This chatbot uses rule-based logic to match keywords in your input."
    )

def default_response(prompt: str) -> str:
    """
    Default fallback when no agent is matched.
    """
    return (
        "🤖 I'm not sure how to respond to that.\n"
        "Try asking about 'server health' or type 'help' for more options."
    )