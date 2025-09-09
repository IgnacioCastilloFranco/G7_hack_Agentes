#CONTENIDO INFORMATIVO Y NARRATIVO
from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.services.madrid_info import get_madrid_location_info
from app.services.storytelling import generate_magical_story
from app.agents.ratoncito_agent import create_ratoncito_agent

router = APIRouter()

class StoryRequest(BaseModel):
    location: str
    children_age_range: Optional[str] = "4-8"  # Por defecto niños pequeños, pero puede ser "9-12", "13-16", etc.
    interests: Optional[List[str]] = None
    previous_locations: Optional[List[str]] = None

class StoryResponse(BaseModel):
    title: str
    content: str
    fun_facts: List[str]
    image_prompts: Optional[List[str]] = None
    
class LocationInfoResponse(BaseModel):
    name: str
    description: str
    historical_data: Dict[str, Any]
    legends: List[Dict[str, str]]
    magical_connection: Optional[str] = None

class LegendRequest(BaseModel):
    location: str
    children_age: Optional[int] = 6
    theme: Optional[str] = None  


@router.get("/locations/{location_name}", response_model=LocationInfoResponse)
async def get_location_info(
    location_name: str,
    with_magic: bool = Query(True, description="Incluir elementos mágicos")
):
    try:
        # Este servicio combina datos reales con elementos mágicos
        info = get_madrid_location_info(location_name, with_magic)
        return info
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Lugar no encontrado: {str(e)}")

@router.post("/stories", response_model=StoryResponse)
async def create_magical_story(request: StoryRequest):
    try:
        story = generate_magical_story(
            location=request.location,
            age_range=request.children_age_range,
            interests=request.interests or ["aventuras", "historia"],
            previous_locations=request.previous_locations
        )
        return story
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando historia: {str(e)}")

@router.post("/legends", response_model=Dict[str, Any])
async def get_location_legends(request: LegendRequest):
    try:
        # Usar directamente el agente para generar leyendas personalizadas
        ratoncito = create_ratoncito_agent()
        
        # Crear prompt específico para leyendas
        prompt = f"Inventa una leyenda mágica sobre {request.location} para niños de {request.children_age} años"
        
        if request.theme:
            prompt += f" con temática de {request.theme}"
        
        # Obtener respuesta del agente
        result = ratoncito.chat(prompt)
        
        # Procesar respuesta
        legend_text = result.get("response", "")
        
        # Extraer título (simplificado - en producción se haría con más precisión)
        title = f"La Leyenda de {request.location}"
        if ": " in legend_text[:50]:  # Buscar posible título al principio
            parts = legend_text.split(": ", 1)
            title = parts[0]
            content = parts[1]
        else:
            content = legend_text
            
        return {
            "title": title,
            "content": content,
            "location": request.location,
            "age_range": f"{request.children_age} años",
            "theme": request.theme,
            "source": "generated_by_ratoncito"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando leyenda: {str(e)}")

@router.get("/search", response_model=List[Dict[str, Any]])
async def search_magical_places(
    query: str = Query(..., description="Término de búsqueda"),
    limit: int = Query(5, description="Número máximo de resultados")
):
    try:
        # Lugares predefinidos (en producción vendrían de base de datos)
        places = [
            {"name": "Palacio Real", "type": "monumento", "magical_level": 5},
            {"name": "Parque del Retiro", "type": "parque", "magical_level": 4},
            {"name": "Plaza Mayor", "type": "plaza", "magical_level": 4},
            {"name": "Puerta del Sol", "type": "plaza", "magical_level": 3},
            {"name": "Museo del Prado", "type": "museo", "magical_level": 5},
            {"name": "Templo de Debod", "type": "monumento", "magical_level": 5},
            {"name": "Gran Vía", "type": "calle", "magical_level": 3},
            {"name": "Mercado de San Miguel", "type": "mercado", "magical_level": 3},
        ]
        
        # Filtrar según query (búsqueda simple)
        query_lower = query.lower()
        filtered_places = [
            place for place in places 
            if query_lower in place["name"].lower() or query_lower in place["type"].lower()
        ][:limit]
        
        # Añadir una descripción mágica a cada lugar
        for place in filtered_places:
            ratoncito = create_ratoncito_agent()
            result = ratoncito.chat(f"Describe brevemente {place['name']} de forma mágica para niños en una frase")
            place["magical_description"] = result.get("response", "")
            
        return filtered_places
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en búsqueda: {str(e)}")

@router.get("/storytelling-elements/{location}", response_model=Dict[str, Any])
async def get_storytelling_elements(
    location: str,
    element_type: str = Query("all", description="Tipo de elemento: characters, objects, magical_events, all")
):
    try:
        # Esta función proporcionaría elementos para que el frontend construya historias interactivas
        
        # Usar el agente para generar elementos narrativos
        ratoncito = create_ratoncito_agent()
        
        if element_type == "characters" or element_type == "all":
            char_prompt = f"Genera 3 personajes mágicos que podrían aparecer en una historia en {location}. Solo nombres y una frase descriptiva para cada uno."
            char_result = ratoncito.chat(char_prompt)
            characters_text = char_result.get("response", "")
            # En producción se haría un parsing más sofisticado de los personajes
            characters = [
                {"name": "Personaje 1", "description": "Descripción..."},
                {"name": "Personaje 2", "description": "Descripción..."},
                {"name": "Personaje 3", "description": "Descripción..."}
            ]
        else:
            characters = []
            
        if element_type == "objects" or element_type == "all":
            obj_prompt = f"Menciona 3 objetos mágicos que podrían encontrarse en {location}"
            obj_result = ratoncito.chat(obj_prompt)
            objects_text = obj_result.get("response", "")
            # En producción se haría un parsing más sofisticado de los objetos
            objects = [
                {"name": "Objeto 1", "power": "Poder mágico..."},
                {"name": "Objeto 2", "power": "Poder mágico..."},
                {"name": "Objeto 3", "power": "Poder mágico..."}
            ]
        else:
            objects = []
            
        if element_type == "magical_events" or element_type == "all":
            event_prompt = f"Describe 2 eventos mágicos que podrían ocurrir en {location}"
            event_result = ratoncito.chat(event_prompt)
            events_text = event_result.get("response", "")
            # En producción se haría un parsing más sofisticado de los eventos
            magical_events = [
                {"name": "Evento 1", "description": "Descripción..."},
                {"name": "Evento 2", "description": "Descripción..."}
            ]
        else:
            magical_events = []
            
        return {
            "location": location,
            "characters": characters,
            "objects": objects,
            "magical_events": magical_events
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando elementos narrativos: {str(e)}")