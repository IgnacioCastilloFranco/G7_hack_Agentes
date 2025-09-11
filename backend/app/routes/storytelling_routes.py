from fastapi import APIRouter, HTTPException, Body, Query, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uuid
from app.routes.agent_routes import get_agent_session 

router = APIRouter()

# ---- MODELOS DE DATOS ----
class GameRequest(BaseModel):
    location: str
    age_range: str = "7-12"
    difficulty: str = "medium"
    game_type: str = "riddle"
    interests: Optional[List[str]] = None
    session_id: str = "default_game_session"

class AnswerRequest(BaseModel):
    game_id: str
    answer: str
    session_id: str = "default_game_session"

games_db = {}


@router.post("/games")
async def create_game(
    request: GameRequest,
    agent_container: Dict[str, Any] = Depends(get_agent_session)
):
    """Crear un juego o acertijo basado en una ubicación usando el agente ReAct."""
    
    game_id = str(uuid.uuid4())[:8]
    agent = agent_container["agent"]
    
    interests_text = ", ".join(request.interests) if request.interests else "historia y aventuras"
    prompt = f"""
    Crea un acertijo mágico sobre {request.location} para niños de {request.age_range} años 
    interesados en {interests_text}. El acertijo debe ser de dificultad {request.difficulty}.
    Incluye también pistas que podría dar el Ratoncito Pérez para ayudar a resolverlo.
    Formato JSON: {{
        "riddle": "El acertijo completo",
        "hints": ["Pista 1", "Pista 2", "Pista 3"],
        "solution": "La solución al acertijo",
        "learning_fact": "Un dato interesante sobre {request.location} para niños"
    }}"""
    
    try:
        result = agent.chat(prompt)
        response_text = result.get("response", "No se me ocurre ningún acertijo ahora mismo.")

        game_data = {
            "id": game_id,
            "title": f"Misterio en {request.location}",
            "instructions": "Resuelve este acertijo para descubrir un secreto mágico",
            "content": response_text, 
            "location": request.location,
            "difficulty": request.difficulty,
            "age_range": request.age_range,
            "answer": "La respuesta correcta" 
        }
        
        games_db[game_id] = game_data
        
        game_data_response = game_data.copy()
        del game_data_response["answer"] 
            
        return game_data_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando juego: {str(e)}")

@router.post("/games/verify")
async def verify_answer(
    request: AnswerRequest,
    agent_container: Dict[str, Any] = Depends(get_agent_session)
):
    """Verifica la respuesta a un acertijo usando el agente ReAct."""
    
    if request.game_id not in games_db:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    
    game = games_db[request.game_id]
    agent = agent_container["agent"]
    
    prompt = f"""
    Evalúa si la respuesta '{request.answer}' es correcta para este acertijo sobre {game['location']}.
    El acertijo era: '{game['content']}'
    La respuesta correcta es: '{game['answer']}'
    
    Responde como el Ratoncito Pérez, sé amable y motivador.
    Si la respuesta es correcta, felicita con entusiasmo.
    Si es incorrecta, da una pista adicional.
    """
    
    try:
        result = agent.chat(prompt)
        feedback = result.get("response", "")
        
        is_correct = "¡correcto!" in feedback.lower() or "¡acertaste!" in feedback.lower()
        
        return {
            "correct": is_correct,
            "feedback": feedback,
            "reward": "¡Has desbloqueado una historia especial!" if is_correct else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verificando respuesta: {str(e)}")

