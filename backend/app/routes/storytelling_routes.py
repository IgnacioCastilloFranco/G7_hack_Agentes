from fastapi import APIRouter, HTTPException, Body, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uuid
from app.agents.ratoncito_agent import create_ratoncito_agent

router = APIRouter()

_ratoncito_agent = None

def get_ratoncito_agent():
    global _ratoncito_agent
    if _ratoncito_agent is None:
        _ratoncito_agent = create_ratoncito_agent()
    return _ratoncito_agent

# Modelos para las solicitudes
class GameRequest(BaseModel):
    location: str
    age_range: str = "7-12"
    difficulty: str = "medium"
    game_type: str = "riddle"
    interests: Optional[List[str]] = None

class AnswerRequest(BaseModel):
    game_id: str
    answer: str

# Diccionario para almacenar juegos, se podría mejorar con una base de datos real
games_db = {}

@router.post("/games")
async def create_game(request: GameRequest):
    """Crear un juego o acertijo basado en una ubicación usando el agente ReAct"""
    
    game_id = str(uuid.uuid4())[:8]
    agent = get_ratoncito_agent()
    
    # Crear el prompt para el agente, se puede ajustar y pasar a otro archivo
    interests_text = ", ".join(request.interests) if request.interests else "historia y aventuras"
    prompt = f"""Crea un acertijo mágico sobre {request.location} para niños de {request.age_range} años 
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
        response_text = result.get("response", "")
        
        # Esto es para el ejemplo
        game_data = {
            "id": game_id,
            "title": f"Misterio en {request.location}",
            "instructions": "Resuelve este acertijo para descubrir un secreto mágico",
            "content": response_text,
            "hints": [
                "Pista 1 (pídesela al Ratoncito)",
                "Pista 2 (pídesela al Ratoncito)",
                "Pista 3 (pídesela al Ratoncito)"
            ],
            "location": request.location,
            "difficulty": request.difficulty,
            "age_range": request.age_range,
            "answer": "La respuesta correcta" # Podríamos extraerlo del Json del agente 
        }
        
        # Guardar 
        games_db[game_id] = game_data
        
        # No devolvemos la respuesta en la API
        game_data_response = game_data.copy()
        if "answer" in game_data_response:
            del game_data_response["answer"]
            
        return game_data_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando juego: {str(e)}")

@router.post("/games/verify")
async def verify_answer(request: AnswerRequest):
    """Verifica la respuesta a un acertijo usando el agente ReAct"""
    
    if request.game_id not in games_db:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    
    game = games_db[request.game_id]
    agent = get_ratoncito_agent()
    
    # Usar el agente para evaluar la respuesta
    prompt = f"""
    Evalúa si la respuesta "{request.answer}" es correcta para este acertijo sobre {game['location']}.
    El acertijo era: "{game['content']}"
    La respuesta correcta es: "{game['answer']}"
    
    Responde como el Ratoncito Pérez, sé amable y motivador incluso si la respuesta es incorrecta.
    Si la respuesta es correcta, felicita al niño con mucho entusiasmo.
    Si es incorrecta, da una pista adicional para ayudar.
    """
    
    try:
        result = agent.chat(prompt)
        feedback = result.get("response", "")
        
        is_correct = "correcta" in feedback.lower() or "acertado" in feedback.lower()
        
        return {
            "correct": is_correct,
            "feedback": feedback,
            "reward": "¡Has desbloqueado una historia especial!" if is_correct else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verificando respuesta: {str(e)}")

@router.get("/trivia/{location}")
async def get_location_trivia(
    location: str,
    count: int = Query(3, description="Número de preguntas"),
    age_range: str = Query("7-12", description="Rango de edad")
):
    """Genera preguntas de trivia sobre una ubicación usando el agente ReAct"""
    
    agent = get_ratoncito_agent()
    
    prompt = f"""
    Crea {count} preguntas de trivia divertidas sobre {location} para niños de {age_range} años.
    Cada pregunta debe tener 4 opciones y una respuesta correcta.
    Incluye datos reales mezclados con elementos mágicos al estilo del Ratoncito Pérez.
    Formato JSON:
    [
        {{
            "question": "Pregunta 1",
            "options": ["Opción 1", "Opción 2", "Opción 3", "Opción 4"],
            "correct": "Opción correcta"
        }},
        ...
    ]
    """
    
    try:
        result = agent.chat(prompt)
        
        # Aquí también deberíamos parsear el JSON real
        questions = [
            {
                "question": f"¿Qué secreto mágico guarda el Ratoncito Pérez en {location}?",
                "options": ["Un diente de oro", "Una varita mágica", "Un mapa del tesoro", "Un libro de hechizos"],
                "correct": "Un mapa del tesoro"
            },
            {
                "question": f"¿En qué año visitó el Ratoncito Pérez {location} por primera vez?",
                "options": ["1697", "1738", "1803", "1922"],
                "correct": "1738"
            },
            {
                "question": f"¿Qué personaje famoso dejó un diente escondido en {location}?",
                "options": ["El Rey Felipe II", "Napoleón Bonaparte", "Mozart", "Velázquez"],
                "correct": "Mozart"
            }
        ]
        
        return questions[:count]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando trivia: {str(e)}")

@router.get("/challenges/{location}")
async def get_location_challenges(
    location: str,
    age_range: str = Query("7-12", description="Rango de edad")
):
    """Genera retos divertidos para hacer en una ubicación"""
    
    agent = get_ratoncito_agent()
    
    prompt = f"""
    Crea 3 retos o actividades divertidas que los niños de {age_range} años pueden hacer cuando visiten {location}.
    Los retos deben ser educativos, seguros y mantener la personalidad mágica del Ratoncito Pérez.
    Cada reto debe incluir:
    1. Un título divertido
    2. Las instrucciones para completarlo
    3. Por qué es especial (conexión con el Ratoncito Pérez)
    """
    
    try:
        result = agent.chat(prompt)
        
        # Simplificado para el ejemplo, otra vez, parsearíamos el JSON real
        return {
            "location": location,
            "challenges": [
                {
                    "title": "Búsqueda del tesoro mágico",
                    "instructions": "Busca tres objetos en forma de círculo, cuadrado y triángulo en " + location,
                    "magic_connection": "El Ratoncito Pérez usa estas formas para marcar sus caminos secretos"
                },
                {
                    "title": "Dibuja lo invisible",
                    "instructions": "Cierra los ojos, escucha los sonidos, y dibuja lo que 'ves' con tus oídos",
                    "magic_connection": "El Ratoncito Pérez ve con sus bigotes cuando está oscuro"
                },
                {
                    "title": "El código secreto",
                    "instructions": "Cuenta cuántas ventanas hay y multiplica por el número de puertas",
                    "magic_connection": "Es el código que usa el Ratoncito para abrir puertas mágicas"
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando retos: {str(e)}")