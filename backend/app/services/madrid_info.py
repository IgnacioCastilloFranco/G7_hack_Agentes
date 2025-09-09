# Servicios de información sobre Madrid
from typing import Dict, List, Any
from app.agents.ratoncito_agent import create_ratoncito_agent

def get_madrid_location_info(location_name: str, with_magic: bool = True) -> Dict[str, Any]:
    # Datos base (colocar aquí lo de supabase o cambiar según se tenga)
    base_info = {
        # ... datos de madrid
    }
    
    # Enriquecer con información mágica del Ratoncito si se solicita
    if with_magic:
        # Aquí usamos el agente existente
        ratoncito = create_ratoncito_agent()
        result = ratoncito.chat(f"Cuéntame algo mágico sobre {location_name}")
        base_info["magical_connection"] = result.get("response", "")
    
    return base_info