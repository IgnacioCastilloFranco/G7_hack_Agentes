import os
import httpx
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

class GooglePlacesService:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_MAPS_API_KEY no encontrada en variables de entorno")
        
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        
    async def search_nearby_cultural_sites(self, latitude: float, longitude: float, radius: int = 5000) -> List[Dict[str, Any]]:
        """
        Busca sitios culturales e históricos cerca de las coordenadas dadas
        
        Args:
            latitude: Latitud de la ubicación
            longitude: Longitud de la ubicación
            radius: Radio de búsqueda en metros (máximo 50000)
            
        Returns:
            Lista de sitios encontrados
        """
        # Tipos de lugares culturales e históricos, yo lo acortaría un poco
        place_types = [
            'museum',
            'tourist_attraction', 
            'church',
            'synagogue',
            'hindu_temple',
            'mosque',
            'place_of_worship',
            'art_gallery',
            'library',
            'university'
        ]
        
        all_places = []
        
        # Buscar por cada tipo de lugar, mejorar también
        for place_type in place_types:
            try:
                places = await self._search_places_by_type(
                    latitude, longitude, radius, place_type
                )
                all_places.extend(places)
            except Exception as e:
                print(f"Error buscando {place_type}: {e}")
                continue
        
        # Eliminamos duplicados basándonos en place_id
        unique_places = {}
        for place in all_places:
            place_id = place.get('place_id')
            if place_id and place_id not in unique_places:
                unique_places[place_id] = place
        
        # Ordenamos, comprobar que funciona bien
        sorted_places = sorted(
            unique_places.values(),
            key=lambda x: (x.get('rating', 0), -x.get('distance', float('inf'))),
            reverse=True
        )
        
        return sorted_places[:20]  # Limitamos a los 20 mejores
    
    async def _search_places_by_type(self, latitude: float, longitude: float, radius: int, place_type: str) -> List[Dict[str, Any]]:
        """
        Busca lugares de un tipo específico usando Google Places Nearby Search
        """
        url = f"{self.base_url}/nearbysearch/json"
        
        params = {
            'location': f"{latitude},{longitude}",
            'radius': min(radius, 50000), 
            'type': place_type,
            'key': self.api_key,
            'language': 'es' 
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') != 'OK':
                print(f"Google Places API error: {data.get('status')} - {data.get('error_message', '')}")
                return []
            
            places = []
            for result in data.get('results', []):
                # Filtrar solo lugares con rating alto y que sean realmente culturales, mejorar
                if self._is_cultural_place(result):
                    place_info = await self._format_place_info(result, latitude, longitude)
                    if place_info:
                        places.append(place_info)
            
            return places
    
    def _is_cultural_place(self, place: Dict[str, Any]) -> bool:
        """
        Determina si un lugar es realmente cultural/histórico basándose en varios criterios
        """
        # Limitamos a lugares con buena valoración
        rating = place.get('rating', 0)
        if rating < 3.5:
            return False
        
        # Y debe tener un número mínimo de valoraciones
        user_ratings_total = place.get('user_ratings_total', 0)
        if user_ratings_total < 10:
            return False
        
        # Intentamos filtrar por tipos
        types = place.get('types', [])
        cultural_types = {
            'museum', 'art_gallery', 'tourist_attraction', 'church', 
            'synagogue', 'hindu_temple', 'mosque', 'place_of_worship',
            'library', 'university', 'establishment', 'point_of_interest'
        }
        
        # Debe tener al menos un tipo cultural
        if not any(t in cultural_types for t in types):
            return False
        
        # Excluimos tipos comerciale, es decir no culturales
        excluded_types = {
            'store', 'shopping_mall', 'restaurant', 'food', 'lodging',
            'gas_station', 'atm', 'bank', 'pharmacy', 'hospital'
        }
        
        if any(t in excluded_types for t in types):
            return False
        
        return True
    
    async def _format_place_info(self, place: Dict[str, Any], user_lat: float, user_lng: float) -> Optional[Dict[str, Any]]:
        """
        Formatea la información del lugar para que coincida con nuestro modelo SiteInfo
        """
        try:
            location = place.get('geometry', {}).get('location', {})
            lat = location.get('lat')
            lng = location.get('lng')
            
            if not lat or not lng:
                return None
            
            # Calculamos distancia aproximada
            distance = self._calculate_distance(user_lat, user_lng, lat, lng)
            
            # Obtenemos la foto si está disponible
            photo_url = None
            photos = place.get('photos', [])
            if photos:
                photo_reference = photos[0].get('photo_reference')
                if photo_reference:
                    photo_url = f"{self.base_url}/photo?maxwidth=400&photoreference={photo_reference}&key={self.api_key}"
            
            return {
                'name': place.get('name', 'Lugar sin nombre'),
                'address': place.get('vicinity', 'Dirección no disponible'),
                'latitude': lat,
                'longitude': lng,
                'description': self._generate_description(
                    tuple(place.get('types', [])), 
                    place.get('name', 'Lugar sin nombre')
                ),
                'rating': place.get('rating'),
                'photo_url': photo_url,
                'place_id': place.get('place_id'),
                'distance': distance,
                'types': place.get('types', [])
            }
        except Exception as e:
            print(f"Error formateando lugar: {e}")
            return None
    
    @lru_cache(maxsize=100)
    def _generate_description(self, place_type_tuple, name) -> str:
        """
        Genera una descripción basada en los tipos y información del lugar
        """
        
        # Mapeo de tipos a descripciones en español
        type_descriptions = {
            'museum': 'Museo con colecciones culturales e históricas',
            'art_gallery': 'Galería de arte con exposiciones',
            'church': 'Iglesia con valor histórico y arquitectónico',
            'tourist_attraction': 'Atracción turística de interés cultural',
            'library': 'Biblioteca con patrimonio cultural',
            'university': 'Universidad con valor histórico y arquitectónico',
            'place_of_worship': 'Lugar de culto con importancia histórica'
        }
        
        # Buscar el tipo más relevante
        for place_type in place_type_tuple:
            if place_type in type_descriptions:
                return type_descriptions[place_type]
        
        return f"Sitio de interés cultural e histórico en {name}"
    
    def _calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """
        Calcula la distancia aproximada entre dos puntos en metros usando la fórmula de Haversine
        """
        import math
        
        # Radio de la Tierra en metros
        R = 6371000
        
        # Convertir grados a radianes
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)
        
        # Fórmula de Haversine
        a = (math.sin(delta_lat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    async def search_places_by_text(self, query: str, latitude: Optional[float] = None, longitude: Optional[float] = None) -> List[Dict[str, Any]]:
        """
        Busca lugares por texto usando Google Places Text Search
        """
        url = f"{self.base_url}/textsearch/json"
        
        params = {
            'query': f"{query} cultural histórico Madrid",
            'key': self.api_key,
            'language': 'es'
        }
        
        if latitude and longitude:
            params['location'] = f"{latitude},{longitude}"
            params['radius'] = 10000  
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') != 'OK':
                print(f"Google Places Text Search error: {data.get('status')} - {data.get('error_message', '')}")
                return []
            
            places = []
            for result in data.get('results', []):
                if self._is_cultural_place(result):
                    place_info = await self._format_place_info(
                        result, 
                        latitude or 40.4168, 
                        longitude or -3.7038
                    )
                    if place_info:
                        places.append(place_info)
            
            return places[:15]  