#CONTENIDO INFORMATIVO Y NARRATIVO
from fastapi import APIRouter, HTTPException, Query, Body, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.services.madrid_info import get_madrid_location_info
from app.services.storytelling import generate_magical_story
from app.routes.agent_routes import get_agent_session 
from app.services.google_places_service import GooglePlacesService

router = APIRouter()

google_places = GooglePlacesService()
class StoryRequest(BaseModel):
    location: str
    children_age_range: Optional[str] = "4-8"  
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
    session_id: str = "default_chat_session" 

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
    # Usamos Depends para obtener el agente de la sesión correcta
    agent_session: Dict[str, Any] = Depends(get_agent_session) 
):
    """
    Inicia o continúa un chat sobre un lugar específico
    """
    try:
        ratoncito_agent = agent_session["agent"]
        
        # El historial de chat ahora se podría gestionar en la sesión, pero lo mantenemos simple por ahora
        full_chat_history = agent_session["session_state"].get("chat_history", [])
        
        # Construimos el prompt
        prompt = f"""
        Contexto Adicional: Estamos hablando específicamente sobre el lugar llamado '{request.place_name}'.
        Mensaje del Usuario: {request.user_message}
        """

        # Llamamos al agente
        result = ratoncito_agent.chat(prompt)
        response_text = result.get("response", "¡Por mis bigotitos! Parece que me he quedado sin palabras...")
        
        full_chat_history.append({"role": "user", "content": request.user_message})
        full_chat_history.append({"role": "assistant", "content": response_text})
        agent_session["session_state"]["chat_history"] = full_chat_history
        
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
        info = get_madrid_location_info(location_name, with_magic)
        return info
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Lugar no encontrado: {str(e)}")

@router.post("/stories", response_model=StoryResponse)
async def create_magical_story(request: StoryRequest):
    try:
        # Este servicio ya es independiente y no necesita al agente
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
async def get_location_legends(
    request: LegendRequest,
    agent_session: Dict[str, Any] = Depends(get_agent_session)
):
    try:
        ratoncito = agent_session["agent"]
        
        prompt = f"Inventa una leyenda mágica sobre {request.location} para niños de {request.children_age} años"
        if request.theme:
            prompt += f" con temática de {request.theme}"
        
        result = ratoncito.chat(prompt)
        legend_text = result.get("response", "")
            
        return {
            "title": f"La Leyenda de {request.location}",
            "content": legend_text,
            "location": request.location,
            "source": "generated_by_ratoncito"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando leyenda: {str(e)}")

