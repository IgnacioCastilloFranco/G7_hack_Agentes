from fastapi import APIRouter, HTTPException, Body, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uuid
from app.services.storytelling import (
    generate_madrid_game, 
    generate_madrid_quiz, 
    get_madrid_adventure_suggestions
)

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
    age_range: str = "medianos" #"pequeños", "medianos", "mayores"
    difficulty: str = "medio" #"fácil", "medio", "difícil"
    game_type: str = "adivinanza" # "adivinanza", "visual", "tesoro", "verdadero_falso", "viaje_tiempo", "personaje", "gastronomia", "trajes"

class QuizRequest(BaseModel):
    topic: str  # "monumentos", "historia", "parques", "museos", "leyendas", "gastronomia"
    age_range: str = "medianos"
    num_questions: int = 3
    previous_topics: Optional[List[str]] = None

class AdventureRequest(BaseModel):
    age_range: str = "medianos"
    visited_locations: Optional[List[str]] = None
    interests: Optional[List[str]] = None  # "historia", "arte", "naturaleza", "leyendas", "gastronomia"

class AnswerRequest(BaseModel):
    game_id: str
    answer: str
    game_type: Optional[str] = "adivinanza"

class GameResponse(BaseModel):
    id: str
    game_title: str
    game_type: str
    age_group: str
    location: str
    full_content: str
    clues: List[str]
    solution: str
    educational_fact: str
    next_suggestion: str
    difficulty_level: str
    estimated_duration: str

# Endpoints
@router.post("/games", response_model=Dict[str, Any])
async def create_madrid_game(request: GameRequest):
    """
    🎮 Crear un juego educativo del Ratoncito Pérez sobre Madrid
    
    Tipos de juegos disponibles:
    - adivinanza: Pistas progresivas sobre un lugar
    - visual: Adivinar lugar por descripción de foto
    - tesoro: Búsqueda del tesoro con pistas
    - verdadero_falso: Detectar la afirmación falsa
    - viaje_tiempo: Lugar en diferentes épocas
    - personaje: Personaje histórico describe su lugar favorito
    - gastronomia: Adivinar platos típicos de Madrid
    - trajes: Juego sobre trajes de chulapo/chulapa
    """
    try:
        # Generar juego usando el servicio
        game_result = generate_madrid_game(
            location=request.location,
            age_range=request.age_range,
            game_type=request.game_type,
            difficulty=request.difficulty
        )
        
        # Generar ID único para tracking
        game_id = str(uuid.uuid4())[:8]
        
        # Preparar respuesta
        response = {
            "id": game_id,
            "game_title": game_result["game_title"],
            "game_type": game_result["game_type"],
            "age_group": game_result["age_group"],
            "location": game_result["location"],
            "full_content": game_result["full_content"],
            "clues": game_result["clues"],
            "solution": game_result["solution"],
            "educational_fact": game_result["educational_fact"],
            "next_suggestion": game_result["next_suggestion"],
            "difficulty_level": game_result["difficulty_level"],
            "estimated_duration": game_result["estimated_duration"],
            "instructions": f"🐭 ¡Hola familia! El Ratoncito Pérez os ha preparado una aventura especial en {request.location}",
            "character": "Ratoncito Pérez - Guía Turístico Mágico de Madrid"
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error generando juego: {str(e)}"
        )

@router.post("/quiz", response_model=Dict[str, Any])
async def create_madrid_quiz(request: QuizRequest):
    """
    📝 Crear un quiz educativo del Ratoncito Pérez sobre Madrid
    
    Temas disponibles:
    - monumentos: Palacio Real, Cibeles, Puerta del Sol, etc.
    - historia: Eventos históricos de Madrid
    - parques: Retiro, Casa de Campo, Jardines, etc.
    - museos: Prado, Reina Sofía, Thyssen, etc.
    - leyendas: Historias mágicas de Madrid
    - gastronomia: Platos típicos madrileños
    """
    try:
        # Validar número de preguntas
        if request.num_questions < 1 or request.num_questions > 5:
            raise HTTPException(
                status_code=400,
                detail="El número de preguntas debe estar entre 1 y 5"
            )
        
        # Generar quiz usando el servicio
        quiz_result = generate_madrid_quiz(
            topic=request.topic,
            age_range=request.age_range,
            num_questions=request.num_questions,
            previous_topics=request.previous_topics
        )
        
        # Generar ID único
        quiz_id = str(uuid.uuid4())[:8]
        
        response = {
            "id": quiz_id,
            "quiz_title": quiz_result["quiz_title"],
            "topic": quiz_result["topic"],
            "age_group": quiz_result["age_group"],
            "full_content": quiz_result["full_content"],
            "questions": quiz_result["questions"],
            "answers": quiz_result["answers"],
            "fun_fact": quiz_result["fun_fact"],
            "total_questions": quiz_result["total_questions"],
            "estimated_duration": quiz_result["estimated_duration"],
            "character": "Ratoncito Pérez - Maestro de Quiz Madrileño"
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generando quiz: {str(e)}"
        )
@router.post("/adventures", response_model=Dict[str, Any])
async def get_adventure_suggestions(request: AdventureRequest):
    """
    🗺️ Obtener sugerencias personalizadas de aventuras en Madrid
    
    El Ratoncito Pérez recomienda lugares según:
    - Edad del grupo familiar
    - Lugares ya visitados (evita repetir)
    - Intereses específicos de la familia
    """
    try:
        # Generar sugerencias usando el servicio
        suggestions_result = get_madrid_adventure_suggestions(
            age_range=request.age_range,
            visited_locations=request.visited_locations,
            interests=request.interests
        )
        
        # Generar ID único
        suggestion_id = str(uuid.uuid4())[:8]
        
        response = {
            "id": suggestion_id,
            "suggestions_title": suggestions_result["suggestions_title"],
            "age_group": suggestions_result["age_group"],
            "full_content": suggestions_result["full_content"],
            "recommended_locations": suggestions_result["recommended_locations"],
            "special_recommendation": suggestions_result["special_recommendation"],
            "personalized": suggestions_result["personalized"],
            "character": "Ratoncito Pérez - Consejero de Aventuras Madrileñas",
            "total_suggestions": len(suggestions_result["recommended_locations"])
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generando sugerencias: {str(e)}"
        )
    
@router.post("/games/verify")
async def verify_game_answer(request: AnswerRequest):
    """
    ✅ Verificar respuesta de un juego
    
    Nota: Implementación básica para frontend.
    En producción se almacenarían las respuestas correctas.
    """
    try:
        # Respuestas comunes correctas (implementación básica)
        common_correct_answers = [
            "palacio real", "retiro", "prado", "cibeles", "sol",
            "gran via", "templo debod", "plaza mayor", "almudena",
            "cocido", "calamares", "churros", "chocolate"
        ]
        
        # Normalizar respuesta del usuario
        user_answer = request.answer.lower().strip()
        
        # Verificación básica
        is_correct = any(answer in user_answer for answer in common_correct_answers)
        
        # Respuestas del Ratoncito Pérez según el resultado
        if is_correct:
            feedback_messages = [
                "¡Por mis bigotitos! ¡Lo has adivinado! Eres tan listo como un ratoncito mágico.",
                "¡Fantástico! El Ratoncito Pérez está muy orgulloso de ti.",
                "¡Correcto! Conoces Madrid tan bien como yo conozco los dientes.",
                "¡Bravo! Tienes alma de explorador madrileño.",
                "¡Excelente! Eres un verdadero detective de Madrid."
            ]
            reward_messages = [
                "Has desbloqueado una curiosidad histórica especial",
                "El Ratoncito Pérez te regala un dato curioso",
                "Has ganado una pista para tu próxima aventura",
                "Desbloqueas una historia mágica de Madrid"
            ]
        else:
            feedback_messages = [
                "¡No pasa nada! El Ratoncito Pérez te ayuda con una pista extra.",
                "¡Casi! Sigue intentándolo, pequeño explorador.",
                "¡Vamos! Tú puedes, tienes madera de aventurero madrileño.",
                "¡No te rindas! Cada intento te acerca más al tesoro."
            ]
            reward_messages = [
                "Tienes una pista extra del Ratoncito Pérez",
                "El Ratoncito te da ánimos para seguir intentándolo",
                "Puedes pedir otra pista si lo necesitas"
            ]
        
        import random
        feedback = random.choice(feedback_messages)
        reward = random.choice(reward_messages)
        
        return {
            "correct": is_correct,
            "feedback": feedback,
            "reward": reward,
            "game_id": request.game_id,
            "character_response": f"🐭 {feedback}"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error verificando respuesta: {str(e)}"
        )

@router.get("/game-types")
async def get_available_game_types():
    """
    📋 Obtener tipos de juegos disponibles con descripciones
    """
    return {
        "game_types": [
            {
                "id": "adivinanza",
                "name": "Adivinanza Descriptiva",
                "description": "Pistas progresivas para adivinar un lugar de Madrid",
                "duration": "5-10 minutos",
                "icon": "🔍"
            },
            {
                "id": "visual", 
                "name": "Foto Misteriosa",
                "description": "Adivinar el lugar describiendo una foto imaginaria",
                "duration": "3-8 minutos",
                "icon": "📸"
            },
            {
                "id": "tesoro",
                "name": "Búsqueda del Tesoro", 
                "description": "Seguir pistas como en una búsqueda del tesoro",
                "duration": "7-12 minutos",
                "icon": "🗺️"
            },
            {
                "id": "verdadero_falso",
                "name": "Detector de Mentiras",
                "description": "Encontrar la afirmación falsa entre 3 opciones",
                "duration": "4-8 minutos", 
                "icon": "🕵️"
            },
            {
                "id": "viaje_tiempo",
                "name": "Máquina del Tiempo",
                "description": "Ver cómo era el lugar en diferentes épocas",
                "duration": "8-15 minutos",
                "icon": "⏰"
            },
            {
                "id": "personaje",
                "name": "Personaje Misterioso",
                "description": "Un personaje histórico habla de su lugar favorito",
                "duration": "6-11 minutos",
                "icon": "👑"
            },
            {
                "id": "gastronomia",
                "name": "Chef Ratoncito",
                "description": "Adivinar platos típicos de Madrid",
                "duration": "5-10 minutos",
                "icon": "🍽️"
            },
            {
                "id": "trajes",
                "name": "Vestidor Madrileño",
                "description": "Juego sobre trajes de chulapo y chulapa",
                "duration": "7-12 minutos",
                "icon": "👗"
            }
        ],
        "age_ranges": [
            {
                "id": "pequeños",
                "name": "Pequeños Exploradores",
                "description": "4-7 años - Juegos simples y divertidos",
                "icon": "🧸"
            },
            {
                "id": "medianos", 
                "name": "Aventureros",
                "description": "8-12 años - Desafíos educativos equilibrados",
                "icon": "🎒"
            },
            {
                "id": "mayores",
                "name": "Expertos",
                "description": "13+ años - Contenido detallado y complejo",
                "icon": "🎓"
            }
        ]
    }

@router.get("/popular-locations")
async def get_popular_madrid_locations():
    """
    📍 Obtener ubicaciones populares de Madrid para juegos
    """
    return {
        "locations": [
            {
                "name": "Palacio Real",
                "category": "monumentos",
                "difficulty": "medio",
                "suitable_games": ["adivinanza", "visual", "viaje_tiempo", "personaje"],
                "description": "Residencia oficial de los Reyes de España"
            },
            {
                "name": "Parque del Retiro", 
                "category": "parques",
                "difficulty": "fácil",
                "suitable_games": ["adivinanza", "tesoro", "visual"],
                "description": "El pulmón verde de Madrid"
            },
            {
                "name": "Museo del Prado",
                "category": "museos", 
                "difficulty": "medio",
                "suitable_games": ["personaje", "verdadero_falso", "viaje_tiempo"],
                "description": "Una de las pinacotecas más importantes del mundo"
            },
            {
                "name": "Puerta del Sol",
                "category": "plazas",
                "difficulty": "fácil",
                "suitable_games": ["adivinanza", "visual", "tesoro"],
                "description": "El kilómetro cero de España"
            },
            {
                "name": "Plaza Mayor",
                "category": "plazas",
                "difficulty": "fácil", 
                "suitable_games": ["adivinanza", "viaje_tiempo", "gastronomia"],
                "description": "Plaza histórica del Madrid de los Austrias"
            },
            {
                "name": "Gran Vía",
                "category": "calles",
                "difficulty": "medio",
                "suitable_games": ["visual", "viaje_tiempo", "trajes"],
                "description": "El Broadway madrileño"
            },
            {
                "name": "Templo de Debod",
                "category": "monumentos",
                "difficulty": "difícil",
                "suitable_games": ["adivinanza", "personaje", "verdadero_falso"],
                "description": "Templo egipcio auténtico en Madrid"
            }
        ]
    }
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