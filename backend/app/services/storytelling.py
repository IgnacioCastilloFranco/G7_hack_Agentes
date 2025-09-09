# Servicio para generar juegos y adivinanzas del Ratoncito Pérez sobre Madrid
from typing import Dict, List, Any, Optional
from app.agents.ratoncito_agent import create_ratoncito_agent

def generate_madrid_game(
    location: str,
    age_range: str,
    game_type: str,
    difficulty: Optional[str] = "medio",
    previous_games: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Genera juegos educativos sobre lugares de Madrid usando el Ratoncito Pérez
    
    Args:
        location: Lugar específico de Madrid (ej: "Palacio Real", "Retiro")
        age_range: Rango de edad ("pequeños", "medianos", "mayores") 
        game_type: Tipo de juego ("adivinanza", "visual", "tesoro", "verdadero_falso", "viaje_tiempo", "personaje")
        difficulty: Nivel de dificultad ("fácil", "medio", "difícil")
        previous_games: Lista de juegos anteriores para evitar repetición
    
    Returns:
        Dict con el juego generado, pistas, solución y datos educativos
    """
    
    context = {
        "location": location,
        "age_range": age_range,
        "game_type": game_type,
        "difficulty": difficulty,
        "previous_games": previous_games or []
    }
    
    # Usar el agente existente con un prompt específico para juegos
    ratoncito = create_ratoncito_agent()
    
    # Crear prompt adaptado para juegos educativos
    prompt = f"""
    Crea un juego tipo "{game_type}" sobre {location} para el grupo de edad "{age_range}".
    Nivel de dificultad: {difficulty}.
    
    Sigue exactamente este formato:
    🐭 ¡Hola! [Saludo]
    🎮 JUEGO: {game_type.title()} - Nivel: {age_range.title()}
    [Contenido del juego con pistas progresivas]
    💡 PISTA EXTRA: [Si necesitan ayuda adicional]
    ✅ SOLUCIÓN: [Respuesta correcta]
    📚 ¿SABÍAIS QUE...?: [Dato educativo interesante]
    🏃‍♀️ PRÓXIMA AVENTURA: [Sugerencia para continuar]
    """
    
    result = ratoncito.chat(prompt, context)
    
    game_content = result.get("response", "")
    
    # Extraer componentes del juego del resultado
    game_components = _parse_game_response(game_content)
    
    return {
        "game_title": f"Aventura del Ratoncito Pérez en {location}",
        "game_type": game_type,
        "age_group": age_range,
        "location": location,
        "full_content": game_content,
        "clues": game_components.get("clues", []),
        "solution": game_components.get("solution", ""),
        "educational_fact": game_components.get("educational_fact", ""),
        "next_suggestion": game_components.get("next_suggestion", ""),
        "difficulty_level": difficulty,
        "estimated_duration": _get_estimated_duration(age_range, game_type)
    }

def generate_madrid_quiz(
    topic: str,
    age_range: str,
    num_questions: int = 3,
    previous_topics: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Genera un quiz educativo sobre Madrid con el Ratoncito Pérez
    
    Args:
        topic: Tema del quiz ("monumentos", "historia", "parques", "museos", "leyendas")
        age_range: Rango de edad ("pequeños", "medianos", "mayores")
        num_questions: Número de preguntas (1-5)
        previous_topics: Temas ya jugados para evitar repetición
    
    Returns:
        Dict con las preguntas, respuestas y explicaciones educativas
    """
    
    context = {
        "topic": topic,
        "age_range": age_range,
        "num_questions": min(num_questions, 5),  # Máximo 5 preguntas
        "previous_topics": previous_topics or []
    }
    
    ratoncito = create_ratoncito_agent()
    
    prompt = f"""
    Crea un quiz de {num_questions} preguntas sobre {topic} de Madrid para niños de edad "{age_range}".
    
    Formato requerido:
    🐭 ¡Hola! Vamos a jugar al quiz del Ratoncito Pérez sobre {topic}!
    
    PREGUNTA 1: [Pregunta adaptada a la edad]
    A) [Opción]
    B) [Opción] 
    C) [Opción]
    
    [Repetir para cada pregunta]
    
    SOLUCIONES:
    1: [Letra correcta] - [Explicación breve]
    [Repetir para cada respuesta]
    
    📚 DATO CURIOSO: [Información interesante sobre el tema]
    """
    
    result = ratoncito.chat(prompt, context)
    quiz_content = result.get("response", "")
    
    quiz_components = _parse_quiz_response(quiz_content)
    
    return {
        "quiz_title": f"Quiz del Ratoncito Pérez: {topic.title()} de Madrid",
        "topic": topic,
        "age_group": age_range,
        "full_content": quiz_content,
        "questions": quiz_components.get("questions", []),
        "answers": quiz_components.get("answers", []),
        "fun_fact": quiz_components.get("fun_fact", ""),
        "total_questions": num_questions,
        "estimated_duration": f"{num_questions * 2}-{num_questions * 3} minutos"
    }

def get_madrid_adventure_suggestions(
    age_range: str,
    visited_locations: Optional[List[str]] = None,
    interests: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Obtiene sugerencias de aventuras en Madrid basadas en edad e intereses
    
    Args:
        age_range: Rango de edad ("pequeños", "medianos", "mayores")
        visited_locations: Lugares ya visitados
        interests: Intereses de la familia ("historia", "arte", "naturaleza", "leyendas", etc.)
    
    Returns:
        Dict con sugerencias personalizadas de lugares y actividades
    """
    
    context = {
        "age_range": age_range,
        "visited_locations": visited_locations or [],
        "interests": interests or []
    }
    
    ratoncito = create_ratoncito_agent()
    
    interests_text = ", ".join(interests) if interests else "aventuras variadas"
    prompt = f"""
    Sugiere 5 lugares de Madrid perfectos para una familia con niños de edad "{age_range}" 
    interesados en {interests_text}.
    
    Lugares ya visitados (evitar): {', '.join(visited_locations) if visited_locations else 'ninguno'}
    
    Formato:
    🐭 ¡Hola! Aquí tenéis mis recomendaciones especiales:
    
    1. [LUGAR]: [Descripción breve y por qué es perfecto para vosotros]
    2. [LUGAR]: [Descripción breve y por qué es perfecto para vosotros]
    [...]
    
    🎯 MI FAVORITO: [Lugar recomendado especialmente con explicación]
    🎮 JUEGO ESPECIAL: [Sugerencia de actividad para hacer allí]
    """
    
    result = ratoncito.chat(prompt, context)
    suggestions_content = result.get("response", "")
    
    return {
        "suggestions_title": f"Aventuras del Ratoncito Pérez para {age_range}",
        "age_group": age_range,
        "full_content": suggestions_content,
        "recommended_locations": _extract_locations(suggestions_content),
        "special_recommendation": _extract_special_recommendation(suggestions_content),
        "personalized": len(interests) > 0 or len(visited_locations) > 0
    }

# Funciones auxiliares para parsear respuestas
def _parse_game_response(content: str) -> Dict[str, Any]:
    """Extrae componentes del juego de la respuesta del agente"""
    components = {
        "clues": [],
        "solution": "",
        "educational_fact": "",
        "next_suggestion": ""
    }
    
    lines = content.split('\n')
        
    for line in lines:
        line = line.strip()
        if line.startswith('Pista'):
            components["clues"].append(line)
        elif line.startswith('✅ SOLUCIÓN:'):
            components["solution"] = line.replace('✅ SOLUCIÓN:', '').strip()
        elif line.startswith('📚 ¿SABÍAIS QUE...?:'):
            components["educational_fact"] = line.replace('📚 ¿SABÍAIS QUE...?:', '').strip()
        elif line.startswith('🏃‍♀️ PRÓXIMA AVENTURA:'):
            components["next_suggestion"] = line.replace('🏃‍♀️ PRÓXIMA AVENTURA:', '').strip()
    
    return components

def _parse_quiz_response(content: str) -> Dict[str, Any]:
    """Extrae componentes del quiz de la respuesta del agente"""
    # Implementar parsing específico para quiz
    return {
        "questions": [],
        "answers": [],
        "fun_fact": ""
    }

def _extract_locations(content: str) -> List[str]:
    """Extrae nombres de lugares de las sugerencias"""
    locations = []
    lines = content.split('\n')
    
    for line in lines:
        if line.strip() and (line[0].isdigit() or '.' in line[:3]):
            # Buscar patrones como "1. PALACIO REAL:" o "• Retiro:"
            if ':' in line:
                location = line.split(':')[0].strip()
                # Limpiar numeración y símbolos
                location = location.lstrip('123456789. •-').strip()
                if location:
                    locations.append(location)
    
    return locations[:5]  # Máximo 5 sugerencias

def _extract_special_recommendation(content: str) -> str:
    """Extrae la recomendación especial del contenido"""
    lines = content.split('\n')
    for line in lines:
        if line.startswith('🎯 MI FAVORITO:'):
            return line.replace('🎯 MI FAVORITO:', '').strip()
    return ""

def _get_estimated_duration(age_range: str, game_type: str) -> str:
    """Calcula duración estimada según edad y tipo de juego"""
    base_times = {
        "pequeños": {"min": 3, "max": 7},
        "medianos": {"min": 5, "max": 10},  
        "mayores": {"min": 8, "max": 15}
    }
    
    multipliers = {
        "adivinanza": 1.0,
        "visual": 0.8,
        "tesoro": 1.2,
        "verdadero_falso": 0.9,
        "viaje_tiempo": 1.3,
        "personaje": 1.1,
        "gastronomia": 1.0,
        "trajes": 1.2  # Incluye tiempo para la actividad del filtro
    }
    
    base = base_times.get(age_range, {"min": 5, "max": 10})
    multiplier = multipliers.get(game_type, 1.0)
    
    min_time = int(base["min"] * multiplier)
    max_time = int(base["max"] * multiplier)
    
    return f"{min_time}-{max_time} minutos"