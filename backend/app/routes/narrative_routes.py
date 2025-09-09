#CONTENIDO INFORMATIVO Y NARRATIVO
from fastapi import APIRouter, HTTPException, Query, Body, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.services.madrid_info import get_madrid_location_info
from app.services.storytelling import generate_magical_story
from app.agents.ratoncito_agent import create_ratoncito_agent
from app.services.google_places_service import GooglePlacesService

router = APIRouter()

google_places = GooglePlacesService()
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

class LocationRequest(BaseModel):
    latitude: float
    longitude: float
    radius: Optional[int] = 5000

class SearchRequest(BaseModel):
    query: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class PlaceChatRequest(BaseModel):
    place_id: str
    place_name: str
    user_message: str = "Cuéntame sobre este lugar"
    chat_history: Optional[List[Dict[str, str]]] = []

def get_ratoncito_agent():
    return create_ratoncito_agent()


# Rutas para lugares
@router.post("/places/nearby", response_model=Dict[str, Any])
async def get_nearby_places(request: LocationRequest):
    """
    Obtiene lugares culturales e históricos cercanos para narrativas contextuales
    """
    try:
        sites = await google_places.search_nearby_cultural_sites(
            request.latitude, 
            request.longitude, 
            request.radius
        )
        
        return {
            "success": True,
            "sites": sites,
            "count": len(sites),
            "message": f"Encontrados {len(sites)} sitios narrativos cercanos"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error obteniendo sitios cercanos: {str(e)}"
        )

@router.post("/places/search", response_model=Dict[str, Any])
async def search_places(request: SearchRequest):
    """
    Busca lugares por texto para narrativas contextuales
    """
    try:
        sites = await google_places.search_places_by_text(
            request.query,
            request.latitude,
            request.longitude
        )
        
        return {
            "success": True,
            "sites": sites,
            "count": len(sites),
            "message": f"Encontrados {len(sites)} sitios narrativos para '{request.query}'"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error en la búsqueda de lugares: {str(e)}"
        )

@router.get("/places/popular", response_model=Dict[str, Any])
async def get_popular_places():
    """
    Obtiene lugares populares en Madrid para narrativas destacadas
    """
    # Coordenadas del centro de Madrid
    madrid_lat = 40.4168
    madrid_lng = -3.7038
    
    try:
        sites = await google_places.search_nearby_cultural_sites(
            madrid_lat,
            madrid_lng,
            7000  # 7km para cubrir el centro histórico
        )
        
        return {
            "success": True,
            "sites": sites[:12],  # Limitamos a los 12 más populares
            "count": min(len(sites), 12),
            "message": "Lugares más populares para narrativas mágicas de Madrid"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error obteniendo lugares populares: {str(e)}"
        )

@router.post("/places/chat", response_model=Dict[str, Any])
async def place_contextual_chat(
    request: PlaceChatRequest,
    ratoncito_agent = Depends(get_ratoncito_agent)
):
    """
    Inicia o continúa un chat sobre un lugar específico
    """
    try:
        # Preparar el contexto para el chat
        place_context = f"""
        Estamos hablando sobre {request.place_name}, un lugar histórico/cultural en Madrid.
        El Ratoncito Pérez conoce muy bien este lugar y puede contar historias mágicas,
        datos históricos interesantes y curiosidades sobre él.
        """
        
        # Prepara el mensaje para el agente
        if not request.chat_history:
            # Primer mensaje en el chat
            prompt = f"""
            {place_context}
            
            El usuario dice: {request.user_message}
            
            Por favor, como Ratoncito Pérez, presenta este lugar de forma mágica y divertida. 
            Menciona 1-2 datos históricos reales, una conexión mágica inventada, y haz una 
            pregunta al final para mantener la conversación interactiva.
            """
        else:
            # Continuación de la conversación
            chat_history_text = "\n".join([
                f"{'Usuario' if msg.get('role') == 'user' else 'Ratoncito'}: {msg.get('content')}"
                for msg in request.chat_history[-5:]  # Últimos 5 mensajes para no sobrecargar
            ])
            
            prompt = f"""
            {place_context}
            
            Historia de la conversación:
            {chat_history_text}
            
            El usuario ahora dice: {request.user_message}
            
            Responde como el Ratoncito Pérez, manteniendo tu personalidad mágica y divertida.
            Sé informativo pero también imaginativo.
            """
        
        # Obtener respuesta del agente
        result = ratoncito_agent.chat(prompt)
        response_text = result.get("response", "¡Por mis bigotitos! Parece que me he quedado sin palabras...")
        
        return {
            "success": True,
            "response": response_text,
            "place_id": request.place_id,
            "place_name": request.place_name
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error en el chat contextual: {str(e)}"
        )
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