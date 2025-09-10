from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from langchain_groq import ChatGroq
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor, create_react_agent
import requests
import json
import time
from app.core.config import settings
from app.utils.ratoncito_prompts import RatoncitoPrompts


class BaseAgent(ABC):
    """Clase base para todos los agentes especializados"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.llm = self._create_llm()
        self.memory = self._create_memory()
        
    def _create_llm(self) -> ChatGroq:
        return ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            model_name=settings.LLM_MODEL
        )
    
    def _create_memory(self) -> ConversationBufferMemory:
        return ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output"
        )
    
    @abstractmethod
    def process_request(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Procesa una solicitud específica del dominio del agente"""
        pass


class WebSearchAgent(BaseAgent):
    """Agente especializado en búsquedas web y recopilación de información externa"""
    
    def __init__(self):
        super().__init__(
            name="WebSearchAgent",
            description="Especialista en búsquedas web y recopilación de información externa sobre Madrid"
        )
        self.search_strategies = {
            'cultural': ['museo', 'centro cultural', 'galería', 'exposición'],
            'historical': ['palacio', 'histórico', 'patrimonio', 'monumento'],
            'transport': ['metro', 'autobús', 'transporte', 'estación'],
            'gastronomy': ['restaurante', 'comida', 'gastronomía', 'mercado'],
            'association': ['asociación', 'fundación', 'centro', 'iniciativas']
        }
    
    def process_request(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Realiza búsquedas web especializadas"""
        try:
            print(f"🌐 WebSearchAgent: Iniciando búsqueda web para: '{query}'")
            
            # Determinar el tipo de búsqueda
            search_type = self._classify_search_type(query)
            print(f"🔍 WebSearchAgent: Tipo de búsqueda clasificado: {search_type}")
            
            # Generar estrategias de búsqueda específicas
            search_queries = self._generate_search_queries(query, search_type)
            print(f"📝 WebSearchAgent: Generadas {len(search_queries)} consultas de búsqueda: {search_queries}")
            
            # Ejecutar búsquedas
            results = self._execute_searches(search_queries)
            print(f"📊 WebSearchAgent: Obtenidos {len(results)} resultados")
            
            # Evaluar y seleccionar el mejor resultado
            best_result = self._select_best_result(results, query)
            print(f"⭐ WebSearchAgent: Mejor resultado con relevancia: {best_result['relevance_score']}")
            print(f"📄 WebSearchAgent: Fuente: {best_result['source']}")
            
            return {
                'success': True,
                'data': best_result,
                'search_type': search_type,
                'agent': self.name
            }
            
        except Exception as e:
            print(f"❌ WebSearchAgent: Error en búsqueda: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'agent': self.name
            }
    
    def _classify_search_type(self, query: str) -> str:
        """Clasifica el tipo de búsqueda basado en la consulta"""
        query_lower = query.lower()
        
        for search_type, keywords in self.search_strategies.items():
            if any(keyword in query_lower for keyword in keywords):
                return search_type
        
        return 'general'
    
    def _generate_search_queries(self, query: str, search_type: str) -> List[str]:
        """Genera múltiples consultas de búsqueda optimizadas"""
        base_queries = [
            f"{query} Madrid",
            f"{query} Madrid información",
            f"{query} Madrid historia",
            f"que es {query} Madrid",
            f"{query} Madrid ubicación dirección"
        ]
        
        # Agregar consultas específicas según el tipo
        if search_type == 'cultural':
            base_queries.extend([
                f"{query} Madrid museo centro cultural",
                f"{query} Madrid exposiciones actividades"
            ])
        elif search_type == 'historical':
            base_queries.extend([
                f"{query} Madrid patrimonio histórico",
                f"{query} Madrid arquitectura construcción"
            ])
        elif search_type == 'association':
            base_queries.extend([
                f"{query} Madrid asociación organización",
                f"{query} Madrid fundación centro"
            ])
        
        return base_queries
    
    def _get_fallback_info(self, query: str) -> Dict[str, Any]:
        """Información de fallback para consultas comunes sobre Madrid"""
        fallback_data = {
            'palacio real': {
                'content': 'El Palacio Real de Madrid fue construido entre 1738 y 1755 durante el reinado de Felipe V, sobre los restos del antiguo Alcázar de Madrid que se incendió en 1734. Fue diseñado por los arquitectos Filippo Juvarra y Giovanni Battista Sacchetti en estilo barroco clasicista.',
                'source': 'Información histórica de Madrid'
            },
            'museo del prado': {
                'content': 'El Museo del Prado fue inaugurado el 19 de noviembre de 1819 como Real Museo de Pinturas y Esculturas. El edificio fue diseñado por Juan de Villanueva en 1785 como Real Gabinete de Historia Natural.',
                'source': 'Historia del Museo del Prado'
            },
            'puerta del sol': {
                'content': 'La Puerta del Sol es una plaza del centro de Madrid desde el siglo XV. Su configuración actual data principalmente del siglo XIX, con la Casa de Correos construida entre 1766-1768.',
                'source': 'Historia de Madrid'
            },
            'estacion de atocha': {
                'content': 'La Estación de Atocha es la principal estación de ferrocarril de Madrid. Inaugurada en 1851, fue reconstruida en 1892 y modernizada en 1992. Se encuentra en el distrito de Arganzuela y es el punto de partida del AVE hacia el sur de España.',
                'source': 'Información de transporte de Madrid'
            }
        }
        
        query_lower = query.lower()
        for key, info in fallback_data.items():
            if key in query_lower:
                print(f"🎯 WebSearchAgent: Usando información de fallback para: {key}")
                return {
                    'content': info['content'],
                    'source': info['source'],
                    'query': query,
                    'relevance_score': 0.8
                }
        
        return None
    
    def _search_wikipedia(self, query: str) -> Dict[str, Any]:
        """Busca información usando múltiples APIs alternativas"""
        try:
            print(f"🔍 WebSearchAgent: Buscando información para: {query}")
            
            # Primero intentar con OpenStreetMap Nominatim para lugares
            osm_result = self._search_openstreetmap(query)
            if osm_result:
                return osm_result
            
            # Luego intentar con Wikipedia usando búsqueda
            wiki_result = self._search_wikipedia_alternative(query)
            if wiki_result:
                return wiki_result
            
            # Como último recurso, usar información estructurada local
            local_result = self._get_structured_local_info(query)
            if local_result:
                return local_result
            
            return None
            
        except Exception as e:
            print(f"💥 WebSearchAgent: Error general en búsqueda: {str(e)}")
            return None
    
    def _search_openstreetmap(self, query: str) -> Dict[str, Any]:
        """Busca información de lugares usando OpenStreetMap Nominatim"""
        try:
            # API de Nominatim para geocodificación y información de lugares
            base_url = "https://nominatim.openstreetmap.org/search"
            
            # Limpiar y preparar la consulta
            clean_query = query.replace('?', '').replace('¿', '').strip()
            search_query = f"{clean_query} Madrid España"
            
            params = {
                'q': search_query,
                'format': 'json',
                'limit': 3,
                'addressdetails': 1,
                'extratags': 1,
                'namedetails': 1
            }
            
            headers = {
                'User-Agent': 'MadridGuideBot/1.0'
            }
            
            response = requests.get(base_url, params=params, headers=headers, timeout=5)
            print(f"📡 WebSearchAgent: OpenStreetMap status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                for place in data:
                    display_name = place.get('display_name', '')
                    place_type = place.get('type', '')
                    
                    if 'madrid' in display_name.lower():
                        # Construir información del lugar
                        info_parts = []
                        
                        if place_type:
                            info_parts.append(f"Tipo: {place_type}")
                        
                        if 'address' in place:
                            address = place['address']
                            if 'road' in address:
                                info_parts.append(f"Ubicación: {address['road']}")
                        
                        content = f"{display_name}. {'. '.join(info_parts)}"
                        
                        if len(content) > 30:
                            print(f"✅ WebSearchAgent: Información encontrada en OpenStreetMap")
                            return {
                                'content': content,
                                'source': 'OpenStreetMap',
                                'query': query,
                                'relevance_score': self._calculate_relevance(content, query)
                            }
            
            return None
            
        except Exception as e:
            print(f"⚠️ WebSearchAgent: Error en OpenStreetMap: {str(e)}")
            return None
    
    def _search_wikipedia_alternative(self, query: str) -> Dict[str, Any]:
        """Método alternativo para Wikipedia usando búsqueda"""
        try:
            # Usar la API de búsqueda de Wikipedia en lugar del endpoint directo
            search_url = "https://es.wikipedia.org/w/api.php"
            
            clean_query = query.replace('?', '').replace('¿', '').strip()
            
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': f"{clean_query} Madrid",
                'srlimit': 2
            }
            
            response = requests.get(search_url, params=params, timeout=5)
            print(f"📡 WebSearchAgent: Wikipedia API status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                if 'query' in data and 'search' in data['query']:
                    for result in data['query']['search']:
                        title = result.get('title', '')
                        snippet = result.get('snippet', '')
                        
                        if snippet and len(snippet) > 30:
                            # Limpiar HTML del snippet
                            import re
                            clean_snippet = re.sub(r'<[^>]+>', '', snippet)
                            
                            content = f"{title}: {clean_snippet}"
                            
                            print(f"✅ WebSearchAgent: Información encontrada en Wikipedia API")
                            return {
                                'content': content,
                                'source': f"Wikipedia - https://es.wikipedia.org/wiki/{title.replace(' ', '_')}",
                                'query': query,
                                'relevance_score': self._calculate_relevance(content, query)
                            }
            
            return None
            
        except Exception as e:
            print(f"⚠️ WebSearchAgent: Error en Wikipedia API: {str(e)}")
            return None
    
    def _get_structured_local_info(self, query: str) -> Dict[str, Any]:
        """Información estructurada local como último recurso"""
        try:
            query_lower = query.lower()
            
            # Base de datos local expandida
            local_info = {
                'palacio real': {
                    'content': 'El Palacio Real de Madrid es la residencia oficial de la Familia Real Española. Construido en el siglo XVIII sobre los restos del antiguo Alcázar, cuenta con más de 3.400 habitaciones y es uno de los palacios más grandes de Europa.',
                    'source': 'Información turística de Madrid'
                },
                'plaza mayor': {
                    'content': 'La Plaza Mayor de Madrid es una plaza porticada de planta rectangular, situada en el centro histórico de la ciudad. Fue construida durante el reinado de Felipe III, entre 1617 y 1619.',
                    'source': 'Historia de Madrid'
                },
                'retiro': {
                    'content': 'El Parque del Retiro es uno de los parques más significativos de Madrid. Creado en el siglo XVII como jardín real, fue declarado Patrimonio de la Humanidad por la UNESCO en 2021.',
                    'source': 'Patrimonio de Madrid'
                },
                'prado': {
                    'content': 'El Museo del Prado es una de las pinacotecas más importantes del mundo. Inaugurado en 1819, alberga principalmente obras de arte europeo de los siglos XVI al XIX.',
                    'source': 'Museos de Madrid'
                },
                'atocha': {
                    'content': 'La Estación de Atocha es la principal estación ferroviaria de Madrid. Inaugurada en 1851 y reconstruida en varias ocasiones, es el punto de partida del AVE hacia el sur de España.',
                    'source': 'Transporte de Madrid'
                },
                'templo de debod': {
                    'content': 'El Templo de Debod es un templo del antiguo Egipto ubicado en Madrid. Fue un regalo de Egipto a España en 1968 como agradecimiento por la ayuda española para salvar los templos de Nubia. Se encuentra en el Parque del Oeste, cerca de la Plaza de España.',
                    'source': 'Monumentos de Madrid'
                },
                'debod': {
                    'content': 'El Templo de Debod es un auténtico templo egipcio del siglo II a.C. dedicado a los dioses Amón e Isis. Fue trasladado piedra a piedra desde Egipto y reconstruido en Madrid en el Parque del Oeste.',
                    'source': 'Patrimonio histórico de Madrid'
                }
            }
            
            for key, info in local_info.items():
                if key in query_lower or any(word in query_lower for word in key.split()):
                    print(f"✅ WebSearchAgent: Usando información local estructurada para: {key}")
                    return {
                        'content': info['content'],
                        'source': info['source'],
                        'query': query,
                        'relevance_score': 0.9
                    }
            
            return None
            
        except Exception as e:
            print(f"⚠️ WebSearchAgent: Error en información local: {str(e)}")
            return None
    
    def _execute_searches(self, queries: List[str]) -> List[Dict[str, Any]]:
        """Ejecuta las búsquedas web"""
        results = []
        
        # Primero intentar con información de fallback
        for query in queries:
            fallback_result = self._get_fallback_info(query)
            if fallback_result:
                results.append(fallback_result)
                continue
        
        # Si ya tenemos resultados de fallback, devolverlos
        if results:
            print(f"✅ WebSearchAgent: Usando {len(results)} resultados de fallback")
            return results
    
    def _search_actividades_culturales(self, query: str) -> List[Dict[str, Any]]:
        """Busca en las APIs de actividades culturales y de bibliotecas"""
        try:
            results = []
            
            # Buscar en actividades culturales
            data_culturales = self._fetch_data('actividades_culturales', self.actividades_culturales_url)
            if data_culturales:
                results.extend(self._process_actividades_data(data_culturales, query, 'Actividades Culturales'))
            
            # Buscar en actividades de bibliotecas
            data_bibliotecas = self._fetch_data('actividades_bibliotecas', self.actividades_bibliotecas_url)
            if data_bibliotecas:
                results.extend(self._process_actividades_data(data_bibliotecas, query, 'Actividades de Bibliotecas'))
            
            # Ordenar por relevancia
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            return results[:5]  # Máximo 5 resultados
            
        except Exception as e:
            print(f"❌ MadridOpenDataAgent: Error buscando actividades: {e}")
            return []
    
    def _process_actividades_data(self, data: Dict, query: str, source_type: str) -> List[Dict[str, Any]]:
        """Procesa datos de actividades culturales"""
        results = []
        query_terms = query.lower().split()
        
        for item in data.get('@graph', []):
            title = item.get('title', '').lower()
            description = item.get('description', '').lower()
            
            # Calcular relevancia
            relevance = 0
            for term in query_terms:
                if term in title:
                    relevance += 3
                elif term in description:
                    relevance += 2
            
            if relevance > 0:
                # Obtener fechas del evento
                fecha_info = ''
                if 'dtstart' in item:
                    fecha_info = f" Fecha: {item['dtstart']}"
                elif 'event-date' in item:
                    fecha_info = f" Fecha: {item['event-date']}"
                
                result = {
                    'title': item.get('title', ''),
                    'content': f"{item.get('title', '')}: {item.get('description', '')}{fecha_info}",
                    'url': item.get('@id', ''),
                    'source': f'Datos Abiertos Madrid - {source_type}',
                    'relevance_score': relevance / len(query_terms),
                    'type': 'actividad'
                }
                results.append(result)
        
        return results
    
    def _search_bibliotecas(self, query: str) -> List[Dict[str, Any]]:
        """Busca en la API de bibliotecas de Madrid"""
        try:
            data = self._fetch_data('bibliotecas', self.bibliotecas_url)
            if not data:
                return []
            
            results = []
            query_terms = query.lower().split()
            
            for item in data.get('@graph', []):
                title = item.get('title', '').lower()
                description = item.get('description', '').lower()
                address = item.get('address', {}).get('street-address', '').lower()
                
                # Calcular relevancia
                relevance = 0
                for term in query_terms:
                    if term in title:
                        relevance += 3
                    elif term in description:
                        relevance += 2
                    elif term in address:
                        relevance += 1
                
                if relevance > 0:
                    location = item.get('location', {})
                    lat = location.get('latitude', '')
                    lon = location.get('longitude', '')
                    
                    # Obtener horarios si están disponibles
                    horarios = ''
                    if 'organization' in item:
                        org = item['organization']
                        if 'schedule' in org:
                            horarios = f" Horarios: {org['schedule']}"
                    
                    result = {
                        'title': item.get('title', ''),
                        'content': f"{item.get('title', '')}: {item.get('description', '')}. Ubicación: {item.get('address', {}).get('street-address', '')}{horarios}",
                        'url': item.get('@id', ''),
                        'source': 'Datos Abiertos Madrid - Bibliotecas',
                        'relevance_score': relevance / len(query_terms),
                        'coordinates': f"{lat},{lon}" if lat and lon else None,
                        'address': item.get('address', {}).get('street-address', ''),
                        'type': 'biblioteca'
                    }
                    results.append(result)
            
            # Ordenar por relevancia
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            return results[:5]  # Máximo 5 resultados
            
        except Exception as e:
            print(f"❌ MadridOpenDataAgent: Error buscando bibliotecas: {e}")
            return []
    
    def _search_edificios_monumentales(self, query: str) -> List[Dict[str, Any]]:
        """Busca en la API de edificios monumentales de Madrid"""
        try:
            data = self._fetch_data('edificios_monumentales', self.edificios_monumentales_url)
            if not data:
                return []
            
            results = []
            query_terms = query.lower().split()
            
            for item in data.get('@graph', []):
                title = item.get('title', '').lower()
                description = item.get('description', '').lower()
                address = item.get('address', {}).get('street-address', '').lower()
                
                # Calcular relevancia
                relevance = 0
                for term in query_terms:
                    if term in title:
                        relevance += 3
                    elif term in description:
                        relevance += 2
                    elif term in address:
                        relevance += 1
                
                if relevance > 0:
                    location = item.get('location', {})
                    lat = location.get('latitude', '')
                    lon = location.get('longitude', '')
                    
                    result = {
                        'title': item.get('title', ''),
                        'content': f"{item.get('title', '')}: {item.get('description', '')}. Ubicación: {item.get('address', {}).get('street-address', '')}",
                        'url': item.get('@id', ''),
                        'source': 'Datos Abiertos Madrid - Edificios Monumentales',
                        'relevance_score': relevance / len(query_terms),
                        'coordinates': f"{lat},{lon}" if lat and lon else None,
                        'address': item.get('address', {}).get('street-address', ''),
                        'type': 'edificio_monumental'
                    }
                    results.append(result)
            
            # Ordenar por relevancia
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            return results[:5]  # Máximo 5 resultados
            
        except Exception as e:
            print(f"❌ MadridOpenDataAgent: Error buscando edificios monumentales: {e}")
            return []
    
    def _search_teatros(self, query: str) -> List[Dict[str, Any]]:
        """Busca en la API de teatros de Madrid"""
        try:
            data = self._fetch_data('teatros', self.teatros_url)
            if not data:
                return []
            
            return self._process_salas_ocio_data(data, query, 'Teatros')
            
        except Exception as e:
            print(f"❌ MadridOpenDataAgent: Error buscando teatros: {e}")
            return []
    
    def _search_cines(self, query: str) -> List[Dict[str, Any]]:
        """Busca en la API de cines y filmotecas de Madrid"""
        try:
            data = self._fetch_data('cines', self.cines_url)
            if not data:
                return []
            
            return self._process_salas_ocio_data(data, query, 'Cines y Filmotecas')
            
        except Exception as e:
            print(f"❌ MadridOpenDataAgent: Error buscando cines: {e}")
            return []
    
    def _search_auditorios(self, query: str) -> List[Dict[str, Any]]:
        """Busca en la API de auditorios y salas de conciertos de Madrid"""
        try:
            data = self._fetch_data('auditorios', self.auditorios_url)
            if not data:
                return []
            
            return self._process_salas_ocio_data(data, query, 'Auditorios y Salas de Conciertos')
            
        except Exception as e:
            print(f"❌ MadridOpenDataAgent: Error buscando auditorios: {e}")
            return []
    
    def _process_salas_ocio_data(self, data: Dict, query: str, source_type: str) -> List[Dict[str, Any]]:
        """Procesa datos de salas de ocio (teatros, cines, auditorios)"""
        results = []
        query_terms = query.lower().split()
        
        for item in data.get('@graph', []):
            title = item.get('title', '').lower()
            description = item.get('description', '').lower()
            address = item.get('address', {}).get('street-address', '').lower()
            
            # Calcular relevancia
            relevance = 0
            for term in query_terms:
                if term in title:
                    relevance += 3
                elif term in description:
                    relevance += 2
                elif term in address:
                    relevance += 1
            
            if relevance > 0:
                location = item.get('location', {})
                lat = location.get('latitude', '')
                lon = location.get('longitude', '')
                
                # Obtener información de contacto
                contacto = ''
                if 'organization' in item:
                    org = item['organization']
                    if 'telephone' in org:
                        contacto = f" Teléfono: {org['telephone']}"
                
                result = {
                    'title': item.get('title', ''),
                    'content': f"{item.get('title', '')}: {item.get('description', '')}. Ubicación: {item.get('address', {}).get('street-address', '')}{contacto}",
                    'url': item.get('@id', ''),
                    'source': f'Datos Abiertos Madrid - {source_type}',
                    'relevance_score': relevance / len(query_terms),
                    'coordinates': f"{lat},{lon}" if lat and lon else None,
                    'address': item.get('address', {}).get('street-address', ''),
                    'type': source_type.lower().replace(' ', '_')
                }
                results.append(result)
        
        # Ordenar por relevancia
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return results[:5]  # Máximo 5 resultados
        
        # Si no hay fallback, intentar búsqueda con APIs mejoradas
        for query in queries[:3]:  # Limitar a 3 consultas para evitar sobrecarga
            enhanced_result = self._search_wikipedia(query)
            if enhanced_result:
                results.append(enhanced_result)
                break  # Con un resultado de las APIs mejoradas es suficiente
        
        # Si Wikipedia no funciona, intentar DuckDuckGo como último recurso
        if not results:
            print(f"🔄 WebSearchAgent: Wikipedia sin resultados, intentando DuckDuckGo...")
            for query in queries[:2]:  # Solo 2 intentos con DuckDuckGo
                try:
                    search_url = "https://api.duckduckgo.com/"
                    params = {
                        'q': query,
                        'format': 'json',
                        'no_html': '1',
                        'skip_disambig': '1'
                    }
                    
                    response = requests.get(search_url, params=params, timeout=6)
                    
                    if response.status_code in [200, 202]:
                        data = response.json()
                        
                        abstract = data.get('Abstract', '') or data.get('AbstractText', '')
                        answer = data.get('Answer', '')
                        source = data.get('AbstractSource', '')
                        related_topics = data.get('RelatedTopics', [])
                        
                        content = abstract or answer
                        
                        # Si no hay abstract o answer, intentar con related topics
                        if not content and related_topics:
                            for topic in related_topics[:2]:
                                if isinstance(topic, dict) and 'Text' in topic:
                                    topic_text = topic['Text']
                                    if len(topic_text) > 30:
                                        content = topic_text
                                        source = topic.get('FirstURL', source)
                                        break
                        
                        if content and len(content) > 30:
                            print(f"✅ WebSearchAgent: Contenido DuckDuckGo encontrado: {len(content)} caracteres")
                            results.append({
                                'content': content,
                                'source': source,
                                'query': query,
                                'relevance_score': self._calculate_relevance(content, query)
                            })
                            break
                            
                except Exception as e:
                    print(f"💥 WebSearchAgent: Error DuckDuckGo '{query}': {str(e)}")
                    continue
        
        return results
    
    def _calculate_relevance(self, content: str, original_query: str) -> float:
        """Calcula la relevancia del contenido respecto a la consulta original"""
        content_lower = content.lower()
        query_words = original_query.lower().split()
        
        matches = sum(1 for word in query_words if word in content_lower)
        return matches / len(query_words) if query_words else 0
    
    def _select_best_result(self, results: List[Dict[str, Any]], original_query: str) -> Dict[str, Any]:
        """Selecciona el mejor resultado basado en relevancia"""
        if not results:
            return {
                'content': f"No se encontró información específica sobre '{original_query}'",
                'source': 'N/A',
                'relevance_score': 0
            }
        
        # Ordenar por relevancia
        sorted_results = sorted(results, key=lambda x: x['relevance_score'], reverse=True)
        return sorted_results[0]


class KnowledgeAgent(BaseAgent):
    """Agente especializado en conocimiento local y base de datos interna"""
    
    def __init__(self):
        super().__init__(
            name="KnowledgeAgent",
            description="Especialista en conocimiento local de Madrid y base de datos interna"
        )
        self.local_knowledge = self._load_local_knowledge()
    
    def process_request(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Busca en el conocimiento local"""
        try:
            result = self._search_local_knowledge(query)
            
            return {
                'success': True,
                'data': result,
                'source': 'local_knowledge',
                'agent': self.name
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'agent': self.name
            }
    
    def _load_local_knowledge(self) -> Dict[str, Dict[str, str]]:
        """Carga el conocimiento local estructurado"""
        return {
            'museo_historia': {
                'keywords': ['museo', 'historia', 'madrid', 'municipal', 'construido', 'cuando'],
                'content': """🏛️ **Museo de Historia de Madrid**

                        📍 **Ubicación**: Calle de Fuencarral, 78

                        📝 **Historia**: El edificio fue construido entre 1721-1726 como Real Hospicio de San Fernando por Pedro de Ribera. Se convirtió en Museo Municipal en 1929 y actualmente es el Museo de Historia de Madrid.

                        🏛️ **Características**:
                        • Arquitectura barroca madrileña
                        • Fachada diseñada por Pedro de Ribera
                        • Antigua sede del Real Hospicio de San Fernando
                        • Museo desde 1929
                        • Colecciones sobre la historia de Madrid

                        🕐 **Horarios**: Martes a domingo de 10:00 a 20:00h
                        💰 **Entrada**: Gratuita"""
                                    },
                                    'ferroviario': {
                                        'keywords': ['ferrocarril', 'tren', 'vapor', 'locomotora', 'estación'],
                                        'content': """🚂 **Centro de Iniciativas Ferroviarias Vapor Madrid**

                        📍 **Ubicación**: Calle Camino de la Depuradora

                        📝 **Descripción**: Asociación sin ánimo de lucro dedicada a la preservación del patrimonio ferroviario español. Se especializa en:

                        • Organización de excursiones en trenes históricos
                        • Mantenimiento de material rodante vintage
                        • Promoción de la cultura ferroviaria
                        • Eventos educativos sobre historia del ferrocarril

                        🚂 **Actividades destacadas**:
                        • Tren de la Fresa (Madrid-Aranjuez)
                        • Tren de Cervantes (Madrid-Alcalá de Henares)
                        • Excursiones con locomotoras de vapor
                        • Talleres de restauración"""
                                    },
                                    'palacio_real': {
                                        'keywords': ['palacio real', 'palacio', 'real'],
                                        'content': """🏰 **Palacio Real de Madrid**

                        📍 **Ubicación**: Calle de Bailén, s/n

                        📝 **Historia**: Construido en el siglo XVIII sobre los restos del antiguo Alcázar de los Austrias. Es la residencia oficial de la Familia Real Española, aunque actualmente solo se usa para ceremonias de Estado.

                        🏛️ **Características**:
                        • Más de 3.400 habitaciones
                        • 135.000 m² de superficie
                        • Uno de los palacios más grandes de Europa
                        • Arquitectura barroca clasicista"""
                                    },
                                    'retiro': {
                                        'keywords': ['retiro', 'parque del retiro', 'parque'],
                                        'content': """🌳 **Parque del Retiro**

                        📍 **Ubicación**: Centro de Madrid

                        📝 **Historia**: Creado en el siglo XVII como jardín real. Declarado Patrimonio de la Humanidad por la UNESCO en 2021.

                        🌟 **Lugares destacados**:
                        • Palacio de Cristal
                        • Estanque Grande
                        • Monumento a Alfonso XII
                        • Jardín de Rosas
                        • Casa de Vacas"""
            }
        }
    
    def _search_local_knowledge(self, query: str) -> Dict[str, Any]:
        """Busca en el conocimiento local usando palabras clave"""
        query_lower = query.lower()
        
        for topic, data in self.local_knowledge.items():
            keywords = data['keywords']
            matched_keywords = [kw for kw in keywords if kw in query_lower]
            
            if matched_keywords:
                return {
                    'content': data['content'],
                    'topic': topic,
                    'found': True
                }
        
        return {
            'content': None,
            'topic': None,
            'found': False
        }


class ContextAgent(BaseAgent):
    """Agente especializado en manejo de contexto y memoria conversacional"""
    
    def __init__(self):
        super().__init__(
            name="ContextAgent",
            description="Especialista en manejo de contexto y memoria conversacional"
        )
        self.current_site_context = None
        self.conversation_history = []
        self.site_keywords = {
            "palacio real": "Palacio Real",
            "plaza mayor": "Plaza Mayor",
            "retiro": "Parque del Retiro",
            "puerta del sol": "Puerta del Sol",
            "calle arenal": "Calle Arenal",
            "centro ferroviario": "Centro de Iniciativas Ferroviarias Vapor Madrid",
            "vapor madrid": "Centro de Iniciativas Ferroviarias Vapor Madrid",
            "callao": "Plaza de Callao",
            "santoña": "Palacio de Santoña",
            "museo de historia": "Museo de Historia de Madrid",
            "museo historia madrid": "Museo de Historia de Madrid",
            "museo municipal": "Museo de Historia de Madrid",
            "museo del prado": "Museo del Prado",
            "prado": "Museo del Prado",
            "museo prado": "Museo del Prado",
            "estacion de atocha": "Estación de Atocha",
            "atocha": "Estación de Atocha",
            "estacion atocha": "Estación de Atocha"
        }
    
    def process_request(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analiza y gestiona el contexto de la conversación"""
        try:
            # Si se proporciona contexto externo, usarlo
            if context and 'site' in context:
                detected_site = context['site']
                self.current_site_context = detected_site
                needs_context = False
            else:
                # Detectar sitio específico en la consulta
                detected_site = self._detect_site_context(query)
                
                # Determinar si necesita contexto adicional
                needs_context = self._needs_context_clarification(query)
            
            # Actualizar historial
            self._update_conversation_history(query, detected_site)
            
            return {
                'success': True,
                'data': {
                    'current_site': self.current_site_context,
                    'detected_site': detected_site,
                    'needs_context': needs_context,
                    'context_suggestion': self._suggest_context_clarification(query) if needs_context else None
                },
                'agent': self.name
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'agent': self.name
            }
    
    def _detect_site_context(self, query: str) -> Optional[str]:
        """Detecta si la pregunta se refiere a un sitio específico"""
        query_lower = query.lower()
        
        # Buscar sitios específicos mencionados
        for keyword, site_name in self.site_keywords.items():
            if keyword in query_lower:
                self.current_site_context = site_name
                return site_name
        
        # Si no se detecta sitio específico pero hay contexto previo
        if self.current_site_context and any(word in query_lower for word in 
                                           ["cuando", "construido", "historia", "año", "fecha", "donde", "como"]):
            return self.current_site_context
        
        return None
    
    def _needs_context_clarification(self, query: str) -> bool:
        """Determina si la consulta necesita aclaración de contexto"""
        query_lower = query.lower()
        
        # Preguntas ambiguas que necesitan contexto
        ambiguous_patterns = [
            "cuando fue construido",
            "donde esta",
            "como llegar",
            "que horario",
            "cuanto cuesta",
            "esta abierto",
            "cuando abre",
            "cuando cierra"
        ]
        
        has_ambiguous_pattern = any(pattern in query_lower for pattern in ambiguous_patterns)
        has_no_specific_site = not self._detect_site_context(query)
        
        return has_ambiguous_pattern and has_no_specific_site
    
    def _suggest_context_clarification(self, query: str) -> str:
        """Sugiere aclaración de contexto"""
        return f"Para responder mejor a tu pregunta '{query}', ¿podrías especificar sobre qué lugar de Madrid te refieres? Por ejemplo: Palacio Real, Plaza Mayor, Parque del Retiro, etc."
    
    def _update_conversation_history(self, query: str, detected_site: Optional[str]):
        """Actualiza el historial de conversación"""
        self.conversation_history.append({
            'query': query,
            'detected_site': detected_site,
            'timestamp': None  # Se podría agregar timestamp real
        })
        
        # Mantener solo los últimos 10 intercambios
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]


class MadridOpenDataAgent:
    """Agente que consulta las APIs de datos abiertos de Madrid"""
    
    def __init__(self):
        # APIs existentes
        self.monumentos_url = "https://datos.madrid.es/egob/catalogo/300356-0-monumentos-ciudad-madrid.json"
        self.museos_url = "https://datos.madrid.es/egob/catalogo/201132-0-museos.json"
        self.salas_estudio_url = "https://datos.madrid.es/egob/catalogo/217921-0-salas-estudio.json"
        self.parques_url = "https://datos.madrid.es/egob/catalogo/200761-0-parques-jardines.json"
        self.templos_catolicos_url = "https://datos.madrid.es/egob/catalogo/209426-0-templos-catolicas.json"
        self.templos_otros_url = "https://datos.madrid.es/egob/catalogo/209434-0-templos-otros.json"
        self.actividades_culturales_url = "https://datos.madrid.es/egob/catalogo/206974-0-agenda-eventos-culturales-100.json"
        self.actividades_bibliotecas_url = "https://datos.madrid.es/egob/catalogo/206717-0-agenda-eventos-bibliotecas.json"
        self.bibliotecas_url = "https://datos.madrid.es/egob/catalogo/201747-0-bibliobuses-bibliotecas.json"
        self.edificios_monumentales_url = "https://datos.madrid.es/egob/catalogo/208844-0-monumentos-edificios.json"
        self.teatros_url = "https://datos.madrid.es/egob/catalogo/208862-7650046-ocio_salas.json"
        self.cines_url = "https://datos.madrid.es/egob/catalogo/208862-7650164-ocio_salas.json"
        self.auditorios_url = "https://datos.madrid.es/egob/catalogo/208862-7650180-ocio_salas.json"
        
        self.cache = {}
        self.cache_expiry = 3600  # 1 hora en segundos
        self.last_fetch = {}
    
    def process_request(self, query: str, context: Dict) -> List[Dict[str, Any]]:
        """Busca información en las APIs de datos abiertos de Madrid"""
        try:
            print(f"🏛️ MadridOpenDataAgent: Buscando en datos abiertos de Madrid para: '{query}'")
            
            results = []
            query_lower = query.lower()
            print(f"🔍 Query procesada: '{query_lower}'")
            
            # Determinar qué APIs consultar basado en la consulta
            search_monumentos = any(word in query_lower for word in ['monumento', 'estatua', 'escultura', 'memorial', 'obelisco'])
            search_museos = any(word in query_lower for word in ['museo', 'galeria', 'exposicion', 'arte'])
            search_salas_estudio = any(word in query_lower for word in ['sala', 'estudio', 'estudiar', 'lectura', 'leer'])
            search_parques = any(word in query_lower for word in ['parque', 'jardin', 'verde', 'naturaleza', 'pasear'])
            search_templos = any(word in query_lower for word in ['iglesia', 'templo', 'catedral', 'basilica', 'capilla', 'religioso'])
            search_actividades = any(word in query_lower for word in ['actividad', 'evento', 'cultural', 'ocio', 'agenda'])
            search_bibliotecas = any(word in query_lower for word in ['biblioteca', 'libro', 'bibliobús'])
            search_edificios = any(word in query_lower for word in ['edificio', 'arquitectura', 'monumental'])
            search_teatros = any(word in query_lower for word in ['teatro', 'obra', 'representacion', 'escena'])
            search_cines = any(word in query_lower for word in ['cine', 'pelicula', 'filmoteca', 'film'])
            search_auditorios = any(word in query_lower for word in ['auditorio', 'concierto', 'musica', 'sala'])
            
            # Si no hay palabras clave específicas, buscar en las principales categorías
            if not any([search_monumentos, search_museos, search_salas_estudio, search_parques, 
                       search_templos, search_actividades, search_bibliotecas, search_edificios,
                       search_teatros, search_cines, search_auditorios]):
                search_monumentos = search_museos = search_parques = True
            
            # Ejecutar búsquedas según las categorías detectadas
            if search_monumentos:
                monumentos_results = self._search_monumentos(query)
                results.extend(monumentos_results)
            
            if search_museos:
                museos_results = self._search_museos(query)
                results.extend(museos_results)
                
            if search_salas_estudio:
                salas_results = self._search_salas_estudio(query)
                results.extend(salas_results)
                
            if search_parques:
                parques_results = self._search_parques(query)
                results.extend(parques_results)
                
            if search_templos:
                templos_results = self._search_templos(query)
                results.extend(templos_results)
                
            if search_actividades:
                actividades_results = self._search_actividades_culturales(query)
                results.extend(actividades_results)
                
            if search_bibliotecas:
                bibliotecas_results = self._search_bibliotecas(query)
                results.extend(bibliotecas_results)
                
            if search_edificios:
                edificios_results = self._search_edificios_monumentales(query)
                results.extend(edificios_results)
                
            if search_teatros:
                teatros_results = self._search_teatros(query)
                results.extend(teatros_results)
                
            if search_cines:
                cines_results = self._search_cines(query)
                results.extend(cines_results)
                
            if search_auditorios:
                auditorios_results = self._search_auditorios(query)
                results.extend(auditorios_results)
            
            print(f"✅ MadridOpenDataAgent: Encontrados {len(results)} resultados")
            return results
            
        except Exception as e:
            print(f"❌ MadridOpenDataAgent: Error: {e}")
            return []
    
    def _search_monumentos(self, query: str) -> List[Dict[str, Any]]:
        """Busca en la API de monumentos de Madrid"""
        try:
            data = self._fetch_data('monumentos', self.monumentos_url)
            if not data:
                return []
            
            results = []
            query_terms = query.lower().split()
            
            for item in data.get('@graph', []):
                title = item.get('title', '').lower()
                description = item.get('description', '').lower()
                address = item.get('address', {}).get('street-address', '').lower()
                
                # Calcular relevancia
                relevance = 0
                for term in query_terms:
                    if term in title:
                        relevance += 3
                    elif term in description:
                        relevance += 2
                    elif term in address:
                        relevance += 1
                
                if relevance > 0:
                    location = item.get('location', {})
                    lat = location.get('latitude', '')
                    lon = location.get('longitude', '')
                    
                    result = {
                        'title': item.get('title', ''),
                        'content': f"{item.get('title', '')}: {item.get('description', '')}. Ubicación: {item.get('address', {}).get('street-address', '')}",
                        'url': item.get('@id', ''),
                        'source': 'Datos Abiertos Madrid - Monumentos',
                        'relevance_score': relevance / len(query_terms),
                        'coordinates': f"{lat},{lon}" if lat and lon else None,
                        'address': item.get('address', {}).get('street-address', ''),
                        'type': 'monumento'
                    }
                    results.append(result)
            
            # Ordenar por relevancia
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            return results[:5]  # Máximo 5 resultados
            
        except Exception as e:
            print(f"❌ MadridOpenDataAgent: Error buscando monumentos: {e}")
            return []
    
    def _search_museos(self, query: str) -> List[Dict[str, Any]]:
        """Busca en la API de museos de Madrid"""
        try:
            data = self._fetch_data('museos', self.museos_url)
            if not data:
                return []
            
            results = []
            query_terms = query.lower().split()
            
            for item in data.get('@graph', []):
                title = item.get('title', '').lower()
                description = item.get('description', '').lower()
                address = item.get('address', {}).get('street-address', '').lower()
                
                # Calcular relevancia
                relevance = 0
                for term in query_terms:
                    if term in title:
                        relevance += 3
                    elif term in description:
                        relevance += 2
                    elif term in address:
                        relevance += 1
                
                if relevance > 0:
                    location = item.get('location', {})
                    lat = location.get('latitude', '')
                    lon = location.get('longitude', '')
                    
                    # Obtener horarios si están disponibles
                    horarios = ''
                    if 'organization' in item:
                        org = item['organization']
                        if 'schedule' in org:
                            horarios = f" Horarios: {org['schedule']}"
                    
                    result = {
                        'title': item.get('title', ''),
                        'content': f"{item.get('title', '')}: {item.get('description', '')}. Ubicación: {item.get('address', {}).get('street-address', '')}{horarios}",
                        'url': item.get('@id', ''),
                        'source': 'Datos Abiertos Madrid - Museos',
                        'relevance_score': relevance / len(query_terms),
                        'coordinates': f"{lat},{lon}" if lat and lon else None,
                        'address': item.get('address', {}).get('street-address', ''),
                        'type': 'museo'
                    }
                    results.append(result)
            
            # Ordenar por relevancia
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            return results[:5]  # Máximo 5 resultados
            
        except Exception as e:
            print(f"❌ MadridOpenDataAgent: Error buscando museos: {e}")
            return []
    
    def _fetch_data(self, data_type: str, url: str) -> Dict:
        """Obtiene datos de la API con cache"""
        current_time = time.time()
        
        # Verificar si tenemos datos en cache y no han expirado
        if (data_type in self.cache and 
            data_type in self.last_fetch and 
            current_time - self.last_fetch[data_type] < self.cache_expiry):
            print(f"📋 MadridOpenDataAgent: Usando cache para {data_type}")
            return self.cache[data_type]
        
        try:
            print(f"🌐 MadridOpenDataAgent: Consultando API de {data_type}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.cache[data_type] = data
                self.last_fetch[data_type] = current_time
                print(f"✅ MadridOpenDataAgent: Datos de {data_type} obtenidos correctamente")
                return data
            else:
                print(f"❌ MadridOpenDataAgent: Error HTTP {response.status_code} para {data_type}")
                return {}
                
        except Exception as e:
            print(f"❌ MadridOpenDataAgent: Error obteniendo {data_type}: {e}")
            return {}
    
    def _search_salas_estudio(self, query: str) -> List[Dict[str, Any]]:
        """Busca en la API de salas de estudio y lectura de Madrid"""
        try:
            data = self._fetch_data('salas_estudio', self.salas_estudio_url)
            if not data:
                return []
            
            results = []
            query_terms = query.lower().split()
            
            for item in data.get('@graph', []):
                title = item.get('title', '').lower()
                description = item.get('description', '').lower()
                address = item.get('address', {}).get('street-address', '').lower()
                
                # Calcular relevancia
                relevance = 0
                for term in query_terms:
                    if term in title:
                        relevance += 3
                    elif term in description:
                        relevance += 2
                    elif term in address:
                        relevance += 1
                
                if relevance > 0:
                    location = item.get('location', {})
                    lat = location.get('latitude', '')
                    lon = location.get('longitude', '')
                    
                    # Obtener horarios si están disponibles
                    horarios = ''
                    if 'organization' in item:
                        org = item['organization']
                        if 'schedule' in org:
                            horarios = f" Horarios: {org['schedule']}"
                    
                    result = {
                        'title': item.get('title', ''),
                        'content': f"{item.get('title', '')}: {item.get('description', '')}. Ubicación: {item.get('address', {}).get('street-address', '')}{horarios}",
                        'url': item.get('@id', ''),
                        'source': 'Datos Abiertos Madrid - Salas de Estudio',
                        'relevance_score': relevance / len(query_terms),
                        'coordinates': f"{lat},{lon}" if lat and lon else None,
                        'address': item.get('address', {}).get('street-address', ''),
                        'type': 'sala_estudio'
                    }
                    results.append(result)
            
            # Ordenar por relevancia
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            return results[:5]  # Máximo 5 resultados
            
        except Exception as e:
            print(f"❌ MadridOpenDataAgent: Error buscando salas de estudio: {e}")
            return []
    
    def _search_parques(self, query: str) -> List[Dict[str, Any]]:
        """Busca en la API de parques y jardines de Madrid"""
        try:
            data = self._fetch_data('parques', self.parques_url)
            if not data:
                return []
            
            results = []
            query_terms = query.lower().split()
            
            for item in data.get('@graph', []):
                title = item.get('title', '').lower()
                description = item.get('description', '').lower()
                address = item.get('address', {}).get('street-address', '').lower()
                
                # Calcular relevancia
                relevance = 0
                for term in query_terms:
                    if term in title:
                        relevance += 3
                    elif term in description:
                        relevance += 2
                    elif term in address:
                        relevance += 1
                
                if relevance > 0:
                    location = item.get('location', {})
                    lat = location.get('latitude', '')
                    lon = location.get('longitude', '')
                    
                    result = {
                        'title': item.get('title', ''),
                        'content': f"{item.get('title', '')}: {item.get('description', '')}. Ubicación: {item.get('address', {}).get('street-address', '')}",
                        'url': item.get('@id', ''),
                        'source': 'Datos Abiertos Madrid - Parques y Jardines',
                        'relevance_score': relevance / len(query_terms),
                        'coordinates': f"{lat},{lon}" if lat and lon else None,
                        'address': item.get('address', {}).get('street-address', ''),
                        'type': 'parque'
                    }
                    results.append(result)
            
            # Ordenar por relevancia
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            return results[:5]  # Máximo 5 resultados
            
        except Exception as e:
            print(f"❌ MadridOpenDataAgent: Error buscando parques: {e}")
            return []
    
    def _search_templos(self, query: str) -> List[Dict[str, Any]]:
        """Busca en las APIs de templos católicos y no católicos de Madrid"""
        try:
            results = []
            
            # Buscar en templos católicos
            data_catolicos = self._fetch_data('templos_catolicos', self.templos_catolicos_url)
            if data_catolicos:
                results.extend(self._process_templos_data(data_catolicos, query, 'Templos Católicos'))
            
            # Buscar en templos no católicos
            data_otros = self._fetch_data('templos_otros', self.templos_otros_url)
            if data_otros:
                results.extend(self._process_templos_data(data_otros, query, 'Templos No Católicos'))
            
            # Ordenar por relevancia
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            return results[:5]  # Máximo 5 resultados
            
        except Exception as e:
            print(f"❌ MadridOpenDataAgent: Error buscando templos: {e}")
            return []
    
    def _process_templos_data(self, data: Dict, query: str, source_type: str) -> List[Dict[str, Any]]:
        """Procesa datos de templos (católicos o no católicos)"""
        results = []
        query_terms = query.lower().split()
        
        for item in data.get('@graph', []):
            title = item.get('title', '').lower()
            description = item.get('description', '').lower()
            address = item.get('address', {}).get('street-address', '').lower()
            
            # Calcular relevancia
            relevance = 0
            for term in query_terms:
                if term in title:
                    relevance += 3
                elif term in description:
                    relevance += 2
                elif term in address:
                    relevance += 1
            
            if relevance > 0:
                location = item.get('location', {})
                lat = location.get('latitude', '')
                lon = location.get('longitude', '')
                
                result = {
                    'title': item.get('title', ''),
                    'content': f"{item.get('title', '')}: {item.get('description', '')}. Ubicación: {item.get('address', {}).get('street-address', '')}",
                    'url': item.get('@id', ''),
                    'source': f'Datos Abiertos Madrid - {source_type}',
                    'relevance_score': relevance / len(query_terms),
                    'coordinates': f"{lat},{lon}" if lat and lon else None,
                    'address': item.get('address', {}).get('street-address', ''),
                    'type': 'templo'
                }
                results.append(result)
        
        return results

    def _search_teatros(self, query: str) -> List[Dict[str, Any]]:
        """Busca en la API de teatros de Madrid"""
        try:
            data = self._fetch_data('teatros', self.teatros_url)
            if not data:
                return []
            
            results = []
            query_terms = query.lower().split()
            
            for item in data.get('@graph', []):
                title = item.get('title', '').lower()
                description = item.get('description', '').lower()
                address = item.get('address', {}).get('street-address', '').lower()
                
                # Calcular relevancia
                relevance = 0
                for term in query_terms:
                    if term in title:
                        relevance += 3
                    elif term in description:
                        relevance += 2
                    elif term in address:
                        relevance += 1
                
                if relevance > 0:
                    location = item.get('location', {})
                    lat = location.get('latitude', '')
                    lon = location.get('longitude', '')
                    
                    result = {
                        'title': item.get('title', ''),
                        'content': f"{item.get('title', '')}: {item.get('description', '')}. Ubicación: {item.get('address', {}).get('street-address', '')}",
                        'url': item.get('@id', ''),
                        'source': 'Datos Abiertos Madrid - Teatros',
                        'relevance_score': relevance / len(query_terms),
                        'coordinates': f"{lat},{lon}" if lat and lon else None,
                        'address': item.get('address', {}).get('street-address', ''),
                        'type': 'teatro'
                    }
                    results.append(result)
            
            # Ordenar por relevancia
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            return results[:5]  # Máximo 5 resultados
            
        except Exception as e:
            print(f"❌ Error buscando teatros: {e}")
            return []

    def _search_cines(self, query: str) -> List[Dict[str, Any]]:
        """Busca en la API de cines de Madrid"""
        try:
            data = self._fetch_data('cines', self.cines_url)
            if not data:
                return []
            
            results = []
            query_terms = query.lower().split()
            
            for item in data.get('@graph', []):
                title = item.get('title', '').lower()
                description = item.get('description', '').lower()
                address = item.get('address', {}).get('street-address', '').lower()
                
                # Calcular relevancia
                relevance = 0
                for term in query_terms:
                    if term in title:
                        relevance += 3
                    elif term in description:
                        relevance += 2
                    elif term in address:
                        relevance += 1
                
                if relevance > 0:
                    location = item.get('location', {})
                    lat = location.get('latitude', '')
                    lon = location.get('longitude', '')
                    
                    result = {
                        'title': item.get('title', ''),
                        'content': f"{item.get('title', '')}: {item.get('description', '')}. Ubicación: {item.get('address', {}).get('street-address', '')}",
                        'url': item.get('@id', ''),
                        'source': 'Datos Abiertos Madrid - Cines',
                        'relevance_score': relevance / len(query_terms),
                        'coordinates': f"{lat},{lon}" if lat and lon else None,
                        'address': item.get('address', {}).get('street-address', ''),
                        'type': 'cine'
                    }
                    results.append(result)
            
            # Ordenar por relevancia
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            return results[:5]  # Máximo 5 resultados
            
        except Exception as e:
            print(f"❌ Error buscando cines: {e}")
            return []

    def _search_auditorios(self, query: str) -> List[Dict[str, Any]]:
        """Busca en la API de auditorios de Madrid"""
        try:
            data = self._fetch_data('auditorios', self.auditorios_url)
            if not data:
                return []
            
            results = []
            query_terms = query.lower().split()
            
            for item in data.get('@graph', []):
                title = item.get('title', '').lower()
                description = item.get('description', '').lower()
                address = item.get('address', {}).get('street-address', '').lower()
                
                # Calcular relevancia
                relevance = 0
                for term in query_terms:
                    if term in title:
                        relevance += 3
                    elif term in description:
                        relevance += 2
                    elif term in address:
                        relevance += 1
                
                if relevance > 0:
                    location = item.get('location', {})
                    lat = location.get('latitude', '')
                    lon = location.get('longitude', '')
                    
                    result = {
                        'title': item.get('title', ''),
                        'content': f"{item.get('title', '')}: {item.get('description', '')}. Ubicación: {item.get('address', {}).get('street-address', '')}",
                        'url': item.get('@id', ''),
                        'source': 'Datos Abiertos Madrid - Auditorios',
                        'relevance_score': relevance / len(query_terms),
                        'coordinates': f"{lat},{lon}" if lat and lon else None,
                        'address': item.get('address', {}).get('street-address', ''),
                        'type': 'auditorio'
                    }
                    results.append(result)
            
            # Ordenar por relevancia
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            return results[:5]  # Máximo 5 resultados
            
        except Exception as e:
            print(f"❌ Error buscando auditorios: {e}")
            return []
    
    def _search_bibliotecas(self, query: str) -> List[Dict[str, Any]]:
        """Busca en la API de bibliotecas de Madrid"""
        try:
            data = self._fetch_data('bibliotecas', self.bibliotecas_url)
            if not data:
                return []
            
            results = []
            query_terms = query.lower().split()
            
            for item in data.get('@graph', []):
                title = item.get('title', '').lower()
                description = item.get('description', '').lower()
                address = item.get('address', {}).get('street-address', '').lower()
                
                # Calcular relevancia
                relevance = 0
                for term in query_terms:
                    if term in title:
                        relevance += 3
                    elif term in description:
                        relevance += 2
                    elif term in address:
                        relevance += 1
                
                if relevance > 0:
                    location = item.get('location', {})
                    lat = location.get('latitude', '')
                    lon = location.get('longitude', '')
                    
                    result = {
                        'title': item.get('title', ''),
                        'content': f"{item.get('title', '')}: {item.get('description', '')}. Ubicación: {item.get('address', {}).get('street-address', '')}",
                        'url': item.get('@id', ''),
                        'source': 'Datos Abiertos Madrid - Bibliotecas',
                        'relevance_score': relevance / len(query_terms),
                        'coordinates': f"{lat},{lon}" if lat and lon else None,
                        'address': item.get('address', {}).get('street-address', ''),
                        'type': 'biblioteca'
                    }
                    results.append(result)
            
            # Ordenar por relevancia
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            return results[:5]  # Máximo 5 resultados
            
        except Exception as e:
            print(f"❌ Error buscando bibliotecas: {e}")
            return []
    
    def _search_edificios_monumentales(self, query: str) -> List[Dict[str, Any]]:
        """Busca en la API de edificios monumentales de Madrid"""
        try:
            data = self._fetch_data('edificios', self.edificios_url)
            if not data:
                return []
            
            results = []
            query_terms = query.lower().split()
            
            for item in data.get('@graph', []):
                title = item.get('title', '').lower()
                description = item.get('description', '').lower()
                address = item.get('address', {}).get('street-address', '').lower()
                
                # Calcular relevancia
                relevance = 0
                for term in query_terms:
                    if term in title:
                        relevance += 3
                    elif term in description:
                        relevance += 2
                    elif term in address:
                        relevance += 1
                
                if relevance > 0:
                    location = item.get('location', {})
                    lat = location.get('latitude', '')
                    lon = location.get('longitude', '')
                    
                    result = {
                        'title': item.get('title', ''),
                        'content': f"{item.get('title', '')}: {item.get('description', '')}. Ubicación: {item.get('address', {}).get('street-address', '')}",
                        'url': item.get('@id', ''),
                        'source': 'Datos Abiertos Madrid - Edificios Monumentales',
                        'relevance_score': relevance / len(query_terms),
                        'coordinates': f"{lat},{lon}" if lat and lon else None,
                        'address': item.get('address', {}).get('street-address', ''),
                        'type': 'edificio_monumental'
                    }
                    results.append(result)
            
            # Ordenar por relevancia
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            return results[:5]  # Máximo 5 resultados
            
        except Exception as e:
            print(f"❌ Error buscando edificios monumentales: {e}")
            return []


class PersonalityAgent(BaseAgent):
    """Agente especializado en mantener la personalidad del Ratoncito Pérez"""
    
    def __init__(self, personality: str = "magical_guide"):
        super().__init__(
            name="PersonalityAgent",
            description="Especialista en mantener la personalidad y tono del Ratoncito Pérez"
        )
        self.personality = personality
        self.prompts = RatoncitoPrompts()
        self.magical_expressions = [
            "¡Por mis bigotitos!",
            "¡Qué ratoncito tan curioso!",
            "¡Secretos mágicos!",
            "¡Una aventura nos espera!",
            "¡Por mis patitas peludas!",
            "¡Qué maravilloso!"
        ]
    
    def process_request(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Aplica la personalidad del Ratoncito Pérez a la respuesta"""
        try:
            response_data = context.get('response_data', '') if context else ''
            
            # Aplicar personalidad mágica
            magical_response = self._apply_magical_personality(response_data, query)
            
            return {
                'success': True,
                'data': {
                    'magical_response': magical_response,
                    'personality_applied': True
                },
                'agent': self.name
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'agent': self.name
            }
    
    def _apply_magical_personality(self, content: str, original_query: str) -> str:
        """Aplica la personalidad mágica del Ratoncito Pérez"""
        if not content:
            return self._generate_fallback_response(original_query)
        
        # Agregar introducción mágica
        magical_intro = self._get_random_expression()
        
        # Agregar elementos mágicos al contenido
        magical_content = self._add_magical_elements(content)
        
        # Agregar cierre mágico
        magical_outro = "¿Te gustaría descubrir más secretos mágicos de Madrid? 🐭✨"
        
        return f"{magical_intro} {magical_content}\n\n{magical_outro}"
    
    def _get_random_expression(self) -> str:
        """Obtiene una expresión mágica aleatoria"""
        import random
        return random.choice(self.magical_expressions)
    
    def _add_magical_elements(self, content: str) -> str:
        """Agrega elementos mágicos al contenido"""
        # Agregar emojis y elementos mágicos
        magical_content = content
        
        # Reemplazar algunos términos con versiones más mágicas
        replacements = {
            "edificio": "castillo encantado",
            "construcción": "creación mágica",
            "visitantes": "aventureros",
            "turistas": "exploradores mágicos"
        }
        
        for original, magical in replacements.items():
            magical_content = magical_content.replace(original, magical)
        
        return magical_content
    
    def _generate_fallback_response(self, query: str) -> str:
        """Genera una respuesta de respaldo con personalidad"""
        return f"¡Por mis bigotitos! Me encanta tu curiosidad sobre Madrid. Aunque no tengo toda la información sobre '{query}' en este momento, puedo contarte que Madrid está llena de secretos mágicos esperando ser descubiertos. ¿Te gustaría que exploremos juntos algún otro rincón encantado de nuestra ciudad? 🐭✨"


class MadridMultiAgentSystem:
    """Sistema coordinador de múltiples agentes especializados"""
    
    def __init__(self, personality: str = "magical_guide"):
        self.web_search_agent = WebSearchAgent()
        self.knowledge_agent = KnowledgeAgent()
        self.context_agent = ContextAgent()
        self.madrid_data_agent = MadridOpenDataAgent()
        self.personality_agent = PersonalityAgent(personality)
        
        print("🐭 Sistema Multi-Agente del Ratoncito Pérez inicializado")
        print(f"📋 Agentes activos: {len(self._get_all_agents())}")
    
    def _get_all_agents(self) -> List[BaseAgent]:
        """Obtiene lista de todos los agentes"""
        return [
            self.web_search_agent,
            self.knowledge_agent,
            self.context_agent,
            self.personality_agent
        ]
    
    def process_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Procesa una consulta usando el sistema multi-agente"""
        try:
            # 1. Análisis de contexto
            context_result = self.context_agent.process_request(query, context)
            
            if not context_result['success']:
                return self._generate_error_response("Error en análisis de contexto")
            
            context_data = context_result['data']
            
            # 2. Si necesita aclaración de contexto, devolver sugerencia
            if context_data['needs_context']:
                suggestion = context_data['context_suggestion']
                personality_result = self.personality_agent.process_request(
                    query, 
                    {'response_data': suggestion}
                )
                return {
                    'response': personality_result['data']['magical_response'],
                    'success': True,
                    'approach': 'context_clarification',
                    'agents_used': ['ContextAgent', 'PersonalityAgent']
                }
            
            # 3. Búsqueda en datos abiertos de Madrid primero
            madrid_data_results = self.madrid_data_agent.process_request(query, context_data)
            
            all_results = []
            agents_used = ['ContextAgent']
            approach = 'madrid_open_data'
            
            if madrid_data_results and len(madrid_data_results) > 0:
                all_results.extend(madrid_data_results)
                agents_used.append('MadridOpenDataAgent')
            else:
                # 4. Búsqueda web como segunda opción
                web_result = self.web_search_agent.process_request(query, context_data)
                agents_used.append('WebSearchAgent')
                approach = 'web_search'
                
                if web_result['success'] and web_result['data']['content']:
                    all_results.append({
                        'content': web_result['data']['content'],
                        'source': 'Web Search',
                        'relevance_score': 1.0
                    })
                else:
                    # 5. Búsqueda en conocimiento local como fallback
                    knowledge_result = self.knowledge_agent.process_request(query)
                    agents_used.append('KnowledgeAgent')
                    approach = 'local_knowledge'
                    
                    if knowledge_result['success'] and knowledge_result['data']['found']:
                        all_results.append({
                            'content': knowledge_result['data']['content'],
                            'source': 'Local Knowledge',
                            'relevance_score': 1.0
                        })
            
            # 6. Aplicar personalidad mágica
            # Preparar contexto con los resultados para PersonalityAgent
            personality_context = {
                'response_data': all_results[0]['content'] if all_results else f"No se encontró información específica sobre '{query}'",
                'search_results': all_results
            }
            personality_result = self.personality_agent.process_request(
                query, personality_context
            )
            agents_used.append('PersonalityAgent')
            
            if not personality_result['success']:
                return self._generate_error_response("Error aplicando personalidad")
            
            final_response = personality_result['data']['magical_response']
            
            return {
                'response': final_response,
                'success': True,
                'approach': approach,
                'agents_used': agents_used,
                'context_info': {
                    'current_site': context_data['current_site'],
                    'detected_site': context_data['detected_site']
                }
            }
            
        except Exception as e:
            print(f"❌ Error en sistema multi-agente: {str(e)}")
            return self._generate_error_response(str(e))
    
    def _generate_error_response(self, error_msg: str) -> Dict[str, Any]:
        """Genera una respuesta de error con personalidad"""
        fallback_response = self.personality_agent._generate_fallback_response("tu consulta")
        
        return {
            'response': fallback_response,
            'success': True,
            'approach': 'error_fallback',
            'agents_used': ['PersonalityAgent'],
            'error': error_msg
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Obtiene el estado del sistema multi-agente"""
        return {
            'total_agents': len(self._get_all_agents()),
            'agents': {
                agent.name: {
                    'description': agent.description,
                    'status': 'active'
                } for agent in self._get_all_agents()
            },
            'current_context': self.context_agent.current_site_context,
            'conversation_history_length': len(self.context_agent.conversation_history)
        }


def create_madrid_multi_agent_system(personality: str = "magical_guide") -> MadridMultiAgentSystem:
    """Factory function para crear el sistema multi-agente"""
    return MadridMultiAgentSystem(personality=personality)