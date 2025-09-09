#CONTENIDO INTERACTIVO Y LÚDICO

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uuid

router = APIRouter()

# Modelos básicos
class GameRequest(BaseModel):
    location: str
    difficulty: str = "medium"
    game_type: str = "riddle"

class AnswerRequest(BaseModel):
    game_id: str
    answer: str

# Endpoints
@router.post("/games")
async def create_game(request: GameRequest):
    #Crear un juego o acertijo basado en una ubicación
    game_id = str(uuid.uuid4())[:8]
    return {
        "id": game_id,
        "title": f"Misterio en {request.location}",
        "instructions": "Resuelve este acertijo para descubrir un secreto mágico",
        "content": f"Soy pequeño y brillante, en {request.location} me escondo. Los reyes me buscaban, ¿qué soy?",
        "hints": [
            "Brillo cuando hay luz",
            "Soy muy valioso",
            "Estoy escondido en un lugar especial"
        ],
        "difficulty": request.difficulty
    }

@router.post("/games/verify")
async def verify_answer(request: AnswerRequest):
    # En producción verificaría la respuesta real
    return {
        "correct": True,  # Siempre correcto para pruebas de frontend
        "feedback": "¡Por mis bigotitos! ¡Lo has adivinado! Eres tan inteligente como un ratoncito mágico.",
        "reward": "Has desbloqueado una historia especial"
    }

@router.get("/trivia/{location}")
async def get_location_trivia(
    location: str,
    count: int = Query(3, description="Número de preguntas")
):
    # Trivia de ejemplo para frontend
    questions = [
        {
            "question": f"¿En qué año se construyó {location}?",
            "options": ["1700", "1738", "1800", "1850"],
            "correct": "1738"
        },
        {
            "question": f"¿Qué famoso personaje visitó {location} en el siglo XVIII?",
            "options": ["Mozart", "Goya", "Napoleón", "Velázquez"],
            "correct": "Mozart"
        },
        {
            "question": f"¿Qué animal mágico vive en {location} según las leyendas?",
            "options": ["Dragón", "Unicornio", "Ratón mágico", "Hada"],
            "correct": "Ratón mágico"
        },
        {
            "question": f"¿Cuántas habitaciones secretas hay en {location}?",
            "options": ["3", "7", "12", "20"],
            "correct": "7"
        }
    ]
    return questions[:count]