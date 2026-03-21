import os
import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

from src.agent.core import CrestaAIAgent
from src.backend.telemetry import telemetry

# Load environment variables (OPENAI_API_KEY, etc.)
load_dotenv()

app = FastAPI(title="Cresta AI Agent Support API", version="1.0.0")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    answer: str
    intermediate_steps: Optional[List[Any]] = None
    trace_id: str

# In-memory session tracking for demonstration
sessions: Dict[str, CrestaAIAgent] = {}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main endpoint for interacting with the AI Agent.
    Handles session management, tracing, and agent invocation.
    """
    trace_id = telemetry.start_trace()
    start_time = time.time()
    
    session_id = request.session_id
    if session_id not in sessions:
        try:
            sessions[session_id] = CrestaAIAgent()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to initialize Agent: {str(e)}")
            
    agent = sessions[session_id]
    
    try:
        # We would typically use LangChain's async methods or a background task
        # but for this demonstration standard invoke is fine.
        result = agent.get_response(request.message)
        
        # In a real app we'd get real token counts from the LLMCallback
        # Here we mock it based on text length for demonstration purposes
        prompt_t = len(request.message) // 4
        comp_t = len(result["answer"]) // 4
        
        latency = (time.time() - start_time) * 1000
        telemetry.log_interaction(trace_id, prompt_t, comp_t, latency)
        
        return ChatResponse(
            answer=result["answer"],
            intermediate_steps=result["intermediate_steps"],
            trace_id=trace_id
        )
    except Exception as e:
        print(f"Error during agent execution: {e}")
        raise HTTPException(status_code=500, detail="Agent failed to respond")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Cresta AI Agent Backend"}
