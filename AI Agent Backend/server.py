# server.py

from fastapi import FastAPI
from pydantic import BaseModel
from main_agent import agent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend (localhost:3000) to call FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        reply = agent.run(req.message)
        return {"reply": reply}
    except Exception as e:
        return {"reply": f"Error: {str(e)}"}
