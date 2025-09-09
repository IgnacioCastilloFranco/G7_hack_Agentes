from fastapi import APIRouter, HTTPException, Body, Query, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from app.agents.ratoncito_agent import create_ratoncito_agent
from app.agents.simple_ratoncito import create_magic_ratoncito_agent
from fastapi.responses import HTMLResponse

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    location: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    
class ChatResponse(BaseModel):
    response: str
    success: bool
    agent_type: str
    extra_info: Optional[Dict[str, Any]] = None

_ratoncito_react = None
_ratoncito_simple = None

def get_react_agent():
    global _ratoncito_react
    if _ratoncito_react is None:
        _ratoncito_react = create_ratoncito_agent()
    return _ratoncito_react

def get_simple_agent():
    global _ratoncito_simple
    if _ratoncito_simple is None:
        _ratoncito_simple = create_magic_ratoncito_agent()
    return _ratoncito_simple

@router.post("/chat/react", response_model=ChatResponse)
async def chat_with_react_agent(request: ChatRequest):
    # Este es el agente del ratoncito usando ReAct.
    try:
        agent = get_react_agent()
        
        # Prepararamos contexto
        context = request.context or {}
        if request.location:
            context["location"] = request.location
            
        # Obtenemos respuesta
        result = agent.chat(request.message, context)
        is_fallback = result.get("approach", "") == "direct_fallback"
        return {
            "response": result.get("response", "¡Por mis bigotitos! Ha ocurrido algo mágico e inesperado."),
            "success": result.get("success", False),
            "agent_type": "react" if not is_fallback else "react_fallback",
            "extra_info": {
                "approach": result.get("approach", "unknown"),
                "fallback_used": is_fallback
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el agente ReAct: {str(e)}")

@router.post("/chat/simple", response_model=ChatResponse)
async def chat_with_simple_agent(request: ChatRequest):
    #Este es para el ratoncito que trabaja por intuición
    try:
        agent = get_simple_agent()
            
        # Obtenemos la respuesta
        result = agent.chat(request.message, request.location)
        
        return {
            "response": result.get("response", "¡Por mis bigotitos! Ha ocurrido algo mágico e inesperado."),
            "success": result.get("success", False),
            "agent_type": "simple",
            "extra_info": {
                "location_detected": result.get("location_detected", None),
                "intent": result.get("intent", "unknown")
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el agente Simple: {str(e)}")



# Extra para comparar respuestas, pero primero trabajemos en las otras.
@router.get("/compare", response_model=Dict[str, Any])
async def compare_agents(
    message: str = Query(..., description="Mensaje para los agentes"),
    location: Optional[str] = Query(None, description="Ubicación (opcional)"),
):
    try:
        # Obtener respuesta del agente ReAct
        react_agent = get_react_agent()
        react_result = react_agent.chat(message, {"location": location} if location else {})
        
        # Obtener respuesta del agente Simple
        simple_agent = get_simple_agent()
        simple_result = simple_agent.chat(message, location)
        
        return {
            "message": message,
            "location": location,
            "react_response": {
                "text": react_result.get("response", "Error en agente ReAct"),
                "success": react_result.get("success", False),
            },
            "simple_response": {
                "text": simple_result.get("response", "Error en agente Simple"),
                "success": simple_result.get("success", False),
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparando agentes: {str(e)}")
    


# Añadir al final del archivo para documentación interactiva

@router.get("/docs", include_in_schema=False)
async def get_interactive_docs():
    """Documentación interactiva para probar los agentes"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ratoncito Pérez - API Test</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            h1 { color: #4a4a4a; text-align: center; }
            .agent-section { border: 1px solid #ddd; padding: 20px; margin: 20px 0; border-radius: 8px; }
            .agent-header { display: flex; justify-content: space-between; align-items: center; }
            textarea { width: 100%; height: 100px; margin: 10px 0; padding: 10px; }
            button { background-color: #4CAF50; color: white; padding: 10px 15px; border: none; cursor: pointer; border-radius: 4px; }
            .response { background-color: #f9f9f9; padding: 15px; border-left: 5px solid #4CAF50; margin-top: 15px; white-space: pre-wrap; }
            .loading { color: #777; font-style: italic; }
            .error { color: #D32F2F; }
            .react-agent { border-color: #2196F3; }
            .react-agent button { background-color: #2196F3; }
            .simple-agent { border-color: #FF9800; }
            .simple-agent button { background-color: #FF9800; }
            .compare { border-color: #9C27B0; }
            .compare button { background-color: #9C27B0; }
            .response-container { display: flex; }
            .response-column { flex: 1; padding: 10px; }
            input[type="text"] { width: 100%; padding: 8px; margin: 5px 0; }
            .emoji { font-size: 24px; margin-right: 10px; }
        </style>
    </head>
    <body>
        <h1>🐭 Ratoncito Pérez - API Test 🐭</h1>
        
        <div class="agent-section react-agent">
            <div class="agent-header">
                <h2><span class="emoji">🧠</span>Agente ReAct</h2>
            </div>
            <div>
                <label for="react-message">Mensaje:</label>
                <textarea id="react-message" placeholder="Escribe tu mensaje para el Ratoncito Pérez..."></textarea>
                <label for="react-location">Ubicación (opcional):</label>
                <input type="text" id="react-location" placeholder="Ej: Palacio Real, Plaza Mayor...">
                <button onclick="sendToReact()">Enviar a ReAct</button>
            </div>
            <div id="react-response" class="response" style="display: none;"></div>
        </div>
        
        <div class="agent-section simple-agent">
            <div class="agent-header">
                <h2><span class="emoji">✨</span>Agente Simple</h2>
            </div>
            <div>
                <label for="simple-message">Mensaje:</label>
                <textarea id="simple-message" placeholder="Escribe tu mensaje para el Ratoncito Pérez..."></textarea>
                <label for="simple-location">Ubicación (opcional):</label>
                <input type="text" id="simple-location" placeholder="Ej: Palacio Real, Plaza Mayor...">
                <button onclick="sendToSimple()">Enviar a Simple</button>
            </div>
            <div id="simple-response" class="response" style="display: none;"></div>
        </div>
        
        <div class="agent-section compare">
            <div class="agent-header">
                <h2><span class="emoji">🔍</span>Comparar Agentes</h2>
            </div>
            <div>
                <label for="compare-message">Mensaje:</label>
                <textarea id="compare-message" placeholder="Escribe tu mensaje para ambos agentes..."></textarea>
                <label for="compare-location">Ubicación (opcional):</label>
                <input type="text" id="compare-location" placeholder="Ej: Palacio Real, Plaza Mayor...">
                <button onclick="compareAgents()">Comparar</button>
            </div>
            <div class="response-container" id="compare-container" style="display: none;">
                <div class="response-column">
                    <h3>ReAct:</h3>
                    <div id="compare-react" class="response"></div>
                </div>
                <div class="response-column">
                    <h3>Simple:</h3>
                    <div id="compare-simple" class="response"></div>
                </div>
            </div>
        </div>

        <script>
            async function sendToReact() {
                const message = document.getElementById('react-message').value;
                const location = document.getElementById('react-location').value;
                const responseEl = document.getElementById('react-response');
                
                if (!message) {
                    alert('Por favor, escribe un mensaje');
                    return;
                }
                
                responseEl.style.display = 'block';
                responseEl.textContent = 'Preguntando al Ratoncito Pérez...';
                
                try {
                    const response = await fetch('/ratoncito/chat/react', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ 
                            message: message,
                            location: location || undefined
                        })
                    });
                    
                    const data = await response.json();
                    responseEl.textContent = data.response || 'No se recibió respuesta';
                } catch (error) {
                    responseEl.textContent = `Error: ${error.message}`;
                    responseEl.classList.add('error');
                }
            }
            
            async function sendToSimple() {
                const message = document.getElementById('simple-message').value;
                const location = document.getElementById('simple-location').value;
                const responseEl = document.getElementById('simple-response');
                
                if (!message) {
                    alert('Por favor, escribe un mensaje');
                    return;
                }
                
                responseEl.style.display = 'block';
                responseEl.textContent = 'Preguntando al Ratoncito Pérez...';
                
                try {
                    const response = await fetch('/ratoncito/chat/simple', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ 
                            message: message,
                            location: location || undefined
                        })
                    });
                    
                    const data = await response.json();
                    responseEl.textContent = data.response || 'No se recibió respuesta';
                } catch (error) {
                    responseEl.textContent = `Error: ${error.message}`;
                    responseEl.classList.add('error');
                }
            }
            
            async function compareAgents() {
                const message = document.getElementById('compare-message').value;
                const location = document.getElementById('compare-location').value;
                const reactEl = document.getElementById('compare-react');
                const simpleEl = document.getElementById('compare-simple');
                const containerEl = document.getElementById('compare-container');
                
                if (!message) {
                    alert('Por favor, escribe un mensaje');
                    return;
                }
                
                containerEl.style.display = 'flex';
                reactEl.textContent = 'Cargando...';
                simpleEl.textContent = 'Cargando...';
                
                try {
                    const queryParams = new URLSearchParams({
                        message: message
                    });
                    
                    if (location) {
                        queryParams.append('location', location);
                    }
                    
                    const response = await fetch(`/ratoncito/compare?${queryParams.toString()}`);
                    const data = await response.json();
                    
                    reactEl.textContent = data.react_response.text || 'No se recibió respuesta';
                    simpleEl.textContent = data.simple_response.text || 'No se recibió respuesta';
                } catch (error) {
                    reactEl.textContent = `Error: ${error.message}`;
                    simpleEl.textContent = `Error: ${error.message}`;
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Nuevos endpoints para búsqueda de sitios de interés

class LocationRequest(BaseModel):
    latitude: float
    longitude: float
    radius: Optional[int] = 1000  # Radio en metros
    
class SiteSearchRequest(BaseModel):
    query: str
    location: Optional[str] = None
    
class SiteInfo(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float
    description: Optional[str] = None
    rating: Optional[float] = None
    photo_url: Optional[str] = None
    place_id: Optional[str] = None
    
class SitesResponse(BaseModel):
    sites: List[SiteInfo]
    success: bool
    message: Optional[str] = None

@router.post("/sites/nearby", response_model=SitesResponse)
async def get_nearby_sites(request: LocationRequest):
    """Buscar sitios de interés por coordenadas geográficas"""
    try:
        # Por ahora devolvemos datos dummy de Madrid
        # TODO: Integrar con Google Places API
        dummy_sites = [
            {
                "name": "Palacio Real de Madrid",
                "address": "Calle de Bailén, s/n, 28071 Madrid",
                "latitude": 40.4179,
                "longitude": -3.7142,
                "description": "Residencia oficial de la Familia Real Española, uno de los palacios más grandes de Europa.",
                "rating": 4.5,
                "photo_url": None,
                "place_id": "palacio_real_madrid"
            },
            {
                "name": "Plaza Mayor",
                "address": "Plaza Mayor, 28012 Madrid",
                "latitude": 40.4155,
                "longitude": -3.7074,
                "description": "Plaza porticada de planta rectangular, uno de los lugares más emblemáticos de Madrid.",
                "rating": 4.4,
                "photo_url": None,
                "place_id": "plaza_mayor_madrid"
            },
            {
                "name": "Puerta del Sol",
                "address": "Puerta del Sol, 28013 Madrid",
                "latitude": 40.4169,
                "longitude": -3.7035,
                "description": "Plaza pública situada en el centro de Madrid, conocida por el reloj de la Casa de Correos.",
                "rating": 4.2,
                "photo_url": None,
                "place_id": "puerta_del_sol_madrid"
            },
            {
                "name": "Parque del Retiro",
                "address": "Plaza de la Independencia, 7, 28001 Madrid",
                "latitude": 40.4153,
                "longitude": -3.6844,
                "description": "Parque histórico y jardín público situado en el centro de Madrid.",
                "rating": 4.6,
                "photo_url": None,
                "place_id": "parque_retiro_madrid"
            }
        ]
        
        # Filtrar por proximidad (simulado)
        # En una implementación real, calcularíamos la distancia real
        sites = [SiteInfo(**site) for site in dummy_sites]
        
        return SitesResponse(
            sites=sites,
            success=True,
            message=f"Encontrados {len(sites)} sitios cerca de las coordenadas proporcionadas"
        )
        
    except Exception as e:
        return SitesResponse(
            sites=[],
            success=False,
            message=f"Error buscando sitios cercanos: {str(e)}"
        )

@router.post("/sites/search", response_model=SitesResponse)
async def search_sites_by_name(request: SiteSearchRequest):
    """Buscar sitios de interés por nombre"""
    try:
        # Datos dummy de sitios de Madrid para búsqueda
        all_sites = [
            {
                "name": "Palacio Real de Madrid",
                "address": "Calle de Bailén, s/n, 28071 Madrid",
                "latitude": 40.4179,
                "longitude": -3.7142,
                "description": "Residencia oficial de la Familia Real Española, uno de los palacios más grandes de Europa.",
                "rating": 4.5,
                "photo_url": None,
                "place_id": "palacio_real_madrid"
            },
            {
                "name": "Plaza Mayor",
                "address": "Plaza Mayor, 28012 Madrid",
                "latitude": 40.4155,
                "longitude": -3.7074,
                "description": "Plaza porticada de planta rectangular, uno de los lugares más emblemáticos de Madrid.",
                "rating": 4.4,
                "photo_url": None,
                "place_id": "plaza_mayor_madrid"
            },
            {
                "name": "Puerta del Sol",
                "address": "Puerta del Sol, 28013 Madrid",
                "latitude": 40.4169,
                "longitude": -3.7035,
                "description": "Plaza pública situada en el centro de Madrid, conocida por el reloj de la Casa de Correos.",
                "rating": 4.2,
                "photo_url": None,
                "place_id": "puerta_del_sol_madrid"
            },
            {
                "name": "Parque del Retiro",
                "address": "Plaza de la Independencia, 7, 28001 Madrid",
                "latitude": 40.4153,
                "longitude": -3.6844,
                "description": "Parque histórico y jardín público situado en el centro de Madrid.",
                "rating": 4.6,
                "photo_url": None,
                "place_id": "parque_retiro_madrid"
            },
            {
                "name": "Museo del Prado",
                "address": "Calle de Ruiz de Alarcón, 23, 28014 Madrid",
                "latitude": 40.4138,
                "longitude": -3.6921,
                "description": "Museo nacional de pintura que exhibe una de las mejores colecciones de arte europeo.",
                "rating": 4.7,
                "photo_url": None,
                "place_id": "museo_prado_madrid"
            },
            {
                "name": "Templo de Debod",
                "address": "Calle de Ferraz, 1, 28008 Madrid",
                "latitude": 40.4240,
                "longitude": -3.7177,
                "description": "Templo egipcio del siglo II a.C. trasladado piedra a piedra desde Egipto.",
                "rating": 4.3,
                "photo_url": None,
                "place_id": "templo_debod_madrid"
            }
        ]
        
        # Filtrar sitios que coincidan con la búsqueda
        query_lower = request.query.lower()
        filtered_sites = [
            site for site in all_sites 
            if query_lower in site["name"].lower() or 
               query_lower in site["description"].lower() or
               query_lower in site["address"].lower()
        ]
        
        sites = [SiteInfo(**site) for site in filtered_sites]
        
        return SitesResponse(
            sites=sites,
            success=True,
            message=f"Encontrados {len(sites)} sitios que coinciden con '{request.query}'"
        )
        
    except Exception as e:
        return SitesResponse(
            sites=[],
            success=False,
            message=f"Error buscando sitios: {str(e)}"
        )