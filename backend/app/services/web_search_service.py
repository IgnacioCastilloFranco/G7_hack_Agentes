import httpx
from typing import List, Dict, Any
import asyncio

class WebSearchService:
    def __init__(self):
        self.base_url = "https://api.duckduckgo.com"
    
    async def search_place_info(self, place_name: str, location: str = "Madrid") -> str:
        """
        Busca información sobre un lugar usando DuckDuckGo
        """
        try:
            query = f"{place_name} {location} historia cultura información"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.duckduckgo.com/",
                    params={
                        'q': query,
                        'format': 'json',
                        'no_html': '1',
                        'skip_disambig': '1'
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    abstract = data.get('Abstract', '')
                    if abstract:
                        return abstract
                    
                    related = data.get('RelatedTopics', [])
                    if related:
                        info_pieces = []
                        for topic in related[:3]:  
                            if isinstance(topic, dict) and 'Text' in topic:
                                info_pieces.append(topic['Text'])
                        return ' '.join(info_pieces)
                
                return f"No se encontró información específica sobre {place_name}"
                
        except Exception as e:
            print(f"Error buscando información web: {e}")
            return f"Error al buscar información sobre {place_name}"