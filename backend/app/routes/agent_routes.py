from fastapi import APIRouter, HTTPException, Body, Depends
from pydantic import BaseModel
from typing import Dict, Any

from app.agents.ratoncito_agent import RatoncitoAgent, ConversationContext

router = APIRouter()

agent_sessions: Dict[str, Dict[str, Any]] = {}

def get_agent_session(session_id: str = "default_session") -> Dict[str, Any]:
    """
    Gestiona la sesión. Crea una nueva si no existe, o recupera la existente.
    """
    if session_id not in agent_sessions:
        print(f"[*] Creando nueva sesión de agente para: {session_id}")
        agent_sessions[session_id] = {
            "agent": RatoncitoAgent(),
            "context": ConversationContext()  
        }
    return agent_sessions[session_id]

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"

class ChatResponse(BaseModel):
    response: str
    success: bool
    session_id: str

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ratoncito(
    request: ChatRequest,
    agent_session: Dict[str, Any] = Depends(get_agent_session)
):
    try:
        agent = agent_session["agent"]
        context = agent_session["context"] 
        
        result = agent.chat(request.message, context)
        
        if result.get("success"):
            context.last_bot_message = result.get("response")

        return ChatResponse(
            response=result.get("response", "¡Por mis bigotitos! Algo mágico ha ocurrido."),
            success=result.get("success", True),
            session_id=request.session_id,
        )
    except Exception as e:
        print(f"❌ Error fatal en el endpoint de chat: {e}")
        raise HTTPException(status_code=500, detail=f"Error en el agente: {e}")