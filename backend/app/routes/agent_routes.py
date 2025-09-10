from fastapi import APIRouter, HTTPException, Body, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional

from app.agents.ratoncito_agent import RatoncitoAgent

router = APIRouter()

# ---- GESTOR DE SESIONES ----
# Este diccionario actuará como nuestra "memoria" para guardar las conversaciones.
# La clave es el session_id y el valor es el agente con su propia memoria.
agent_sessions: Dict[str, RatoncitoAgent] = {}

def get_agent_session(session_id: str = "default_session") -> Dict[str, Any]:
    """
    Esta es la función clave que faltaba.
    Crea un nuevo agente si la sesión es nueva, o recupera el existente.
    Esto permite que el Ratoncito recuerde la conversación.
    """
    if session_id not in agent_sessions:
        print(f"[*] Creando nueva sesión de agente para: {session_id}")
        agent_sessions[session_id] = RatoncitoAgent()
    
    # Devuelve el agente para que otras rutas puedan usarlo.
    # Usamos un diccionario para poder añadir más cosas en el futuro si es necesario.
    return {"agent": agent_sessions[session_id]}

# ---- MODELOS DE DATOS ----
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"

class ChatResponse(BaseModel):
    response: str
    success: bool
    session_id: str

# ---- ENDPOINT PRINCIPAL DE CHAT ----
@router.post("/chat", response_model=ChatResponse)
async def chat_with_ratoncito(
    request: ChatRequest,
    # Usamos Depends para obtener el agente de la sesión correcta
    agent_container: Dict[str, Any] = Depends(get_agent_session)
):
    """
    Endpoint unificado para chatear con el Ratoncito Pérez.
    Gestiona la memoria y el contexto a través del session_id.
    """
    try:
        agent = agent_container["agent"]
        
        # Unificamos el mensaje y el contexto para el agente
        full_input = f"Mensaje del Usuario: '{request.message}'"

        # Llamamos al agente
        result = agent.chat(full_input)
        
        return ChatResponse(
            response=result.get("response", "¡Por mis bigotitos! Algo mágico ha ocurrido y me he quedado sin palabras."),
            success=result.get("success", False),
            session_id=request.session_id,
        )
    except Exception as e:
        # Si algo falla, intentamos una búsqueda web como último recurso
        print(f"❌ Error en el agente ReAct: {e}")
        try:
            agent = agent_container["agent"]
            fallback_response = agent.web_search(request.message)
            return ChatResponse(
                response=fallback_response,
                success=False,
                session_id=request.session_id,
            )
        except Exception as fallback_e:
            print(f"❌ Error también en el fallback: {fallback_e}")
            raise HTTPException(status_code=500, detail=f"Error fatal en el agente: {e}")