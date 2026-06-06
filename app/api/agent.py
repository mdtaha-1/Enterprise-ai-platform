from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.agent import run_agent

router = APIRouter()

class AgentRequest(BaseModel):
    message: str

@router.post("/run")
async def run_agent_endpoint(request: AgentRequest):
    response = run_agent(request.message)
    return {"response": response}