from fastapi import APIRouter, HTTPException, Body, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
import os

from app.agents.ratoncito_agent import RatoncitoAgent, ConversationContext
from app.services.tts_service import tts_service

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

class TTSRequest(BaseModel):
    text: str
    voice_id: Optional[str] = None
    model_id: str = "eleven_multilingual_v2"
    stability: Optional[float] = 0.5
    similarity_boost: Optional[float] = 0.8
    speed: Optional[float] = 1.0

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

@router.post("/speak")
async def text_to_speech(request: TTSRequest):
    """
    Convierte texto a audio usando ElevenLabs.
    Retorna el archivo de audio como respuesta.
    """
    try:
        # Generar audio usando el servicio TTS
        audio_file_path = tts_service.text_to_speech(
            text=request.text,
            voice_id=request.voice_id,
            model_id=request.model_id,
            stability=request.stability,
            similarity_boost=request.similarity_boost,
            speed=request.speed
        )
        
        # Retornar el archivo de audio
        return FileResponse(
            audio_file_path,
            media_type="audio/mpeg",
            filename=f"ratoncito_audio_{os.path.basename(audio_file_path)}",
            headers={"Content-Disposition": "attachment"}
        )
        
    except Exception as e:
        print(f"❌ Error en TTS: {e}")
        raise HTTPException(status_code=500, detail=f"Error generando audio: {str(e)}")

@router.get("/voices")
async def get_available_voices():
    """
    Obtiene las voces disponibles en ElevenLabs.
    """
    try:
        voices = tts_service.get_available_voices()
        return {"voices": voices, "success": True}
    except Exception as e:
        print(f"❌ Error obteniendo voces: {e}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo voces: {str(e)}")