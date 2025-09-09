# Servicio para generar historias, cambiar según se decida.

from typing import Dict, List, Any, Optional
from app.agents.ratoncito_agent import create_ratoncito_agent

def generate_magical_story(
    location: str,
    age_range: str,
    interests: List[str],
    previous_locations: Optional[List[str]] = None
) -> Dict[str, Any]:
    
    context = {
        "location": location,
        "age_range": age_range,
        "interests": interests,
        "previous_locations": previous_locations or []
    }
    
    # Usar el agente existente con un prompt específico
    ratoncito = create_ratoncito_agent()
    prompt = f"Crea una historia mágica sobre {location} para niños de {age_range} años interesados en {', '.join(interests)}"
    
    result = ratoncito.chat(prompt, context)
    
    story_text = result.get("response", "")
    
    return {
        "title": f"Aventura en {location}",
        "content": story_text,
        "fun_facts": ["Dato curioso 1", "Dato curioso 2"],
        "image_prompts": [f"Ilustración mágica de {location} con el Ratoncito Pérez"]
    }