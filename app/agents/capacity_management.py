# app/agents/capacity_management.py

try:
    import psutil
except ImportError:
    psutil = None

async def server_health(prompt: str) -> str:
    """
    Simulates a server health check. Returns CPU and memory usage.
    If psutil is not available, returns a default message.
    """
    if psutil:
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            mem = psutil.virtual_memory().percent
            return f"✅ Server Health:\nCPU Usage: {cpu}%\nMemory Usage: {mem}%"
        except Exception as e:
            return f"⚠️ Could not fetch live metrics due to an internal error: {e}"
    else:
        return "✅ Server Health: All systems are operational. (Simulated response)"