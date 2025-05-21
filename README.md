# 🧠 Agentic AI Chatbot Backend

This is a **rule-based chatbot backend** built using **FastAPI**, designed to simulate agentic AI behavior without using any LLMs. It routes user messages to specialized agent functions based on trigger phrases (factory pattern), with built-in **content moderation** (profanity and spam filtering).

This project is **modular**, **extensible**, and **ready to be integrated with a React frontend**.

## 📁 Project Structure

```
.
├── app/
│   ├── main.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── capacity_management.py
│   │   └── support.py
│   └── filters/
│       ├── __init__.py
│       └── content_check.py
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/agentic-chatbot-backend.git
cd agentic-chatbot-backend
```

### 2. Set Up Python Environment

Using **virtualenv** (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🧪 Running the Server

Run the FastAPI app using **uvicorn**:

```bash
uvicorn app.main:app --reload
```

This will start the server at:

```
http://localhost:8000
```

## 🛠 API Usage

### POST `/chat`

**Description:** Accepts a user message, performs content checks, and dispatches to the appropriate agent.

**Request:**
```json
{
  "message": "Check server health"
}
```

**Response:**
```json
{
  "response": "✅ Server Health: CPU usage at 42%, Memory usage at 68%",
  "agent": "server health"
}
```

## 🧹 Agent Behavior

Agents are selected based on keyword matching:

| Trigger Phrase    | Agent Function                       |
|------------------|--------------------------------------|
| `server health`  | `capacity_management.server_health`  |
| `help`           | `support.help`                       |
| *none matched*   | `support.default_response`           |

## 🔒 Content Moderation

Handled via `app/filters/content_check.py`:
- ✅ Profanity filtering (via `better_profanity`)
- 🚫 Basic spam detection (repetition, long text, scam phrases)

## 🌐 CORS Support

CORS is enabled to allow requests from a React frontend running on a different port (`http://localhost:3000`).

## 📦 Example Test (Optional)

Using `curl`:
```bash
curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Show me the server health"}'
```

## 📌 To-Do (Future Scope)

- Switch to LLM-based decision logic (Langchain or OpenAI API)
- Add more agents (e.g., weather, ticket status, anomaly detection)
- Support context-aware conversations

## 🧑‍💻 Author

Developed by [Your Name] – rule-based AI enthusiast and full-stack dev.
