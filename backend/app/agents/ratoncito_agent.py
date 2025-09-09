from langchain.agents import AgentExecutor, create_react_agent
from langchain_groq import ChatGroq
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from typing import List, Dict, Any
import os
import requests
import json
from app.core.config import settings
from app.utils.ratoncito_prompts import RatoncitoPrompts
import random

# AgentExecutor: Es como el "cerebro ejecutivo" del agente
# - Toma decisiones sobre qué herramientas usar
# - Controla el flujo de la conversación
# - Maneja errores y límites de iteraciones

# create_react_agent: Es la "fábrica" que ensambla el agente
# - ReAct = Reasoning + Acting (Razonamiento + Acción)
# - Sigue el patrón: Piensa → Actúa → Observa → Repite


# Primero vamos a crear el agente del Ratoncito Pérez
# Este agente usará el modelo Groq y tendrá una personalidad específica definida que pusimos en los prompts
class RatoncitoAgent:
    def __init__(self, personality: str = None):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY no está configurada en .env")

        self.personality = personality or settings.RATONCITO_PERSONALITY
        self.llm = self.create_llm()
        self.memory = self.create_memory()
        self.tools = self.create_tools()
        self.agent = self.create_agent()
        self.agent_executor = self.create_agent_executor()

        print(f"🐭 Ratoncito Pérez inicializado con personalidad: {self.personality}")
        print(f"🧠 Modelo: {settings.LLM_MODEL}")

    def create_llm(self) -> ChatGroq:
        return ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            model_name=settings.LLM_MODEL   
        )
    
    def create_memory(self) -> ConversationBufferMemory:
        return ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output"
        )
    
    def create_tools(self) -> List[Tool]:
        # Aquí vamos a definir las herramientas que el agente puede usar
        return [
            Tool(
                name="saludo_magico",
                description="Usa SOLO cuando alguien te saluda por PRIMERA vez. Genera un saludo mágico del Ratoncito Pérez, mágico y encantador.",
                func=self.magical_greeting
            ),
            Tool(
                name="informacion_madrid",
                description="Úsala SOLO cuando pregunten sobre lugares específicos de Madrid como Palacio Real, Plaza Mayor, Retiro.",
                func=self.madrid_info
            ),
            Tool(
                name="busqueda_especializada",
                description="Realiza búsquedas especializadas para lugares específicos o poco conocidos de Madrid",
                func=self.specialized_search
            ),
            Tool(
                name="contexto_historico_cultural",
                description="Usa cuando necesites proporcionar información histórica y cultural detallada sobre un sitio específico de Madrid. Incluye historia, arquitectura, curiosidades y elementos mágicos.",
                func=self.historical_cultural_context
            ),
            Tool(
                name="busqueda_web",
                description="Usa cuando necesites buscar información actualizada en internet sobre Madrid, eventos, noticias, horarios, o cualquier información que no tengas disponible localmente.",
                func=self.web_search
            ),
            Tool(
                name="documentos_madrid",
                description="Usa cuando necesites información específica sobre transporte público, lugares emblemáticos, gastronomía, festividades o gestión turística de Madrid. Contiene documentos especializados.",
                func=self.get_madrid_documents
            )
        ]
    
    def create_agent(self):
        return create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=RatoncitoPrompts.get_ultra_reliable_react_prompt(),
        )
    
    def create_agent_executor(self) -> AgentExecutor:
        return AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=settings.AGENT_VERBOSE,
            max_iterations=settings.AGENT_MAX_ITERATIONS,
            handle_parsing_errors=True,
            early_stopping_method="generate",  
            return_intermediate_steps=False
            )
    
    # Herramientas del Ratoncito Pérez
    def magical_greeting(self, input_text: str="") -> str:
        return "¡Por mis bigotitos! ¡Hola, pequeños aventureros! Soy el Ratoncito Pérez, guardián mágico de Madrid. 🐭✨"
        # greetings = [
        #     "¡Hola, aventureros! 🐭✨ Soy el Ratoncito Pérez y estoy aquí para mostrarles los secretos mágicos de Madrid. ¿Están listos para una aventura increíble?",
        #     "¡Por mis bigotitos! ¡Qué alegría conoceros! 🎭 Soy el guardián de las historias más fantásticas de Madrid. ¿Me acompañáis en esta aventura mágica?",
        #     "¡Secretos mágicos os esperan! 🏰 Soy el Ratoncito Pérez, y conozco cada rincón encantado de esta hermosa ciudad. ¿Qué lugar os gustaría explorar primero?"
        # ]
        # return random.choice(greetings)
    
    def madrid_info(self, place: str) -> str:
        places = {
            "palacio real": "¡Por mis bigotitos! El Palacio Real es una joya arquitectónica donde vivían los reyes. ¡Tiene más de 3000 habitaciones! Yo tengo mi propia habitación secreta ahí donde guardo los dientes más especiales que me dais... 🏰 ¿Sabéis que por las noches los cuadros cobran vida?",
            "plaza mayor": "¡Qué lugar tan mágico! La Plaza Mayor es como el corazón de Madrid, donde se celebraban fiestas y mercados. ¡He visto tantas celebraciones desde mis escondites en los balcones! Por las noches de luna llena, bajamos todos los ratones y organizamos bailes secretos... 🎉",
            "retiro": "¡Mi jardín favorito! El Parque del Retiro es donde me gusta pasear cuando no estoy recogiendo dientes. Tiene un Palacio de Cristal mágico donde viven mariposas de otros mundos, y muchos árboles centenarios donde escondo sorpresas para los niños más buenos... 🌳 ¿Os gustaría encontrar alguna?",
            "puerta del sol": "¡El centro de toda España! La Puerta del Sol es donde está el kilómetro 0, desde aquí se miden todas las distancias del país. Yo tengo túneles secretos que conectan con todas las calles de Madrid... ⭐ ¡Por mis bigotitos, qué aventuras he vivido ahí!",
            "calle arenal": "¡Mi hogar dulce hogar! En la Calle Arenal tengo mi casita muy especial, en el número 8. Ahí es donde guardo todos los dientes de leche más preciados y donde escribo las historias mágicas de todos los niños de Madrid... 🏠 ¿Os gustaría visitarla algún día?"
        }

        for key, info in places.items():
            if key in place.lower():
                return info
        return f"¡Qué lugar tan interesante mencionas! Aunque no tengo información específica sobre '{place}', puedo contarte que Madrid está lleno de lugares mágicos. ¿Te gustaría que te hable del Palacio Real o la Plaza Mayor?"
    
    def historical_cultural_context(self, site_name: str) -> str:
        """Proporciona contexto histórico y cultural detallado sobre un sitio específico"""
        site_lower = site_name.lower()
        
        historical_contexts = {
            "palacio real": {
                "history": "Construido en el siglo XVIII sobre las ruinas del antiguo Alcázar de los Austrias, que se quemó en 1734. Felipe V ordenó su construcción al arquitecto Filippo Juvarra.",
                "architecture": "Estilo barroco italiano con 3418 habitaciones, siendo uno de los palacios más grandes de Europa. Sus salones están decorados con frescos de Tiepolo y Mengs.",
                "curiosities": "La Armería Real alberga una de las mejores colecciones de armas del mundo. La Farmacia Real conserva frascos y fórmulas de los siglos XVIII y XIX.",
                "magic": "Por las noches, cuando la luna llena ilumina sus ventanas, los retratos de los reyes susurran secretos del pasado. En mi habitación secreta del ático, guardo los dientes de leche de todos los príncipes y princesas que vivieron aquí."
            },
            "plaza mayor": {
                "history": "Construida durante el reinado de Felipe III (1617-1619) por Juan Gómez de Mora. Era el centro de la vida social madrileña, donde se celebraban corridas de toros, autos de fe y coronaciones.",
                "architecture": "Arquitectura herreriana con 237 balcones que rodean la plaza rectangular. La Casa de la Panadería destaca por sus frescos alegóricos.",
                "curiosities": "Tiene 9 puertas de acceso y ha sufrido tres grandes incendios. El mercado navideño se celebra aquí desde 1860.",
                "magic": "En las noches de invierno, cuando nieva, los fantasmas de los antiguos comerciantes siguen vendiendo sus mercancías. Desde los balcones, las damas de antaño aún observan las festividades que ya no existen."
            },
            "parque del retiro": {
                "history": "Creado en el siglo XVII como jardín real para Felipe IV. Abierto al público en 1868. Era el lugar de recreo de la realeza española.",
                "architecture": "El Palacio de Cristal (1887) es una joya del hierro y cristal inspirada en el Crystal Palace de Londres. El Estanque Grande tiene un monumento a Alfonso XII.",
                "curiosities": "Tiene más de 15,000 árboles de 167 especies diferentes. El Ángel Caído es una de las pocas estatuas del mundo dedicadas al diablo.",
                "magic": "En el Palacio de Cristal viven mariposas de otros mundos que solo aparecen al amanecer. Los árboles centenarios guardan los deseos de miles de niños en sus raíces, y yo los ayudo a que se cumplan."
            },
            "puerta del sol": {
                "history": "Desde el siglo XV era una de las puertas de la muralla medieval. Se convirtió en el centro neurálgico de Madrid y de España, siendo el kilómetro 0 de las carreteras radiales.",
                "architecture": "La Casa de Correos (1768) alberga el famoso reloj de las campanadas de Año Nuevo. La placa del kilómetro 0 marca el centro geográfico de España.",
                "curiosities": "El oso y el madroño, símbolo de Madrid, se encuentra aquí desde 1967. Las campanadas de fin de año se retransmiten desde aquí desde 1962.",
                "magic": "Bajo la Puerta del Sol existe una red de túneles secretos que conecta con toda la ciudad. Desde ahí, nosotros los ratones mágicos podemos llegar a cualquier casa de Madrid en segundos para recoger los dientes de leche."
            },
            "museo del prado": {
                "history": "Inaugurado en 1819 como Real Museo de Pinturas. Fue diseñado por Juan de Villanueva como Gabinete de Ciencias Naturales para Carlos III.",
                "architecture": "Neoclásico con fachada de granito y ladrillo. Las ampliaciones de Rafael Moneo (2007) duplicaron su espacio expositivo.",
                "curiosities": "Alberga la mejor colección de pintura española del mundo, con obras de Velázquez, Goya y El Greco. 'Las Meninas' es su obra más famosa.",
                "magic": "Por las noches, los personajes de los cuadros cobran vida y organizan tertulias secretas. Velázquez me enseñó a pintar retratos en miniatura de todos los niños de Madrid."
            },
            "teatro real": {
                "history": "Inaugurado en 1850 durante el reinado de Isabel II. Tardó 32 años en construirse y fue uno de los teatros de ópera más importantes de Europa.",
                "architecture": "Estilo neoclásico con una cúpula de hierro innovadora para su época. Tiene 1746 localidades distribuidas en seis plantas.",
                "curiosities": "Ha sido teatro, casino, conservatorio y sala de conciertos. La restauración de 1997 lo devolvió a su esplendor original.",
                "magic": "Los fantasmas de las grandes divas siguen cantando en el escenario durante las noches de luna llena. En los palcos superiores, las almas de los melómanos del siglo XIX aún aplauden las mejores actuaciones."
            }
        }
        
        # Buscar coincidencias en el nombre del sitio
        for key, context in historical_contexts.items():
            if key in site_lower or any(word in site_lower for word in key.split()):
                return f"""¡Por mis bigotitos! Te voy a contar la historia mágica de este lugar extraordinario... ✨

🏛️ **Historia**: {context['history']}

🎨 **Arquitectura**: {context['architecture']}

🔍 **Curiosidades**: {context['curiosities']}

✨ **Secretos Mágicos**: {context['magic']}

¿Te gustaría que te cuente más secretos sobre este lugar encantado? ¡Tengo tantas historias guardadas en mi casita de la Calle Arenal! 🐭"""
        
        # Si no encuentra información específica, proporciona una respuesta genérica mágica
        return f"""¡Por mis bigotitos! Aunque '{site_name}' es un lugar muy especial, no tengo todos los detalles mágicos guardados en mi memoria. Pero puedo contarte que cada rincón de Madrid tiene su propia historia encantada... ✨

¿Te gustaría que te hable de alguno de mis lugares favoritos como el Palacio Real, la Plaza Mayor, o el Parque del Retiro? ¡Tengo historias fascinantes sobre todos ellos! 🐭🏰"""

    def web_search(self, query: str) -> str:
        """Realiza una búsqueda web para obtener información actualizada usando múltiples estrategias"""
        try:
            # Estrategia 1: Búsqueda específica con términos relacionados
            search_terms = [
                f"{query} Madrid información",
                f"{query} Madrid historia",
                f"{query} Madrid ubicación dirección",
                f"{query} Madrid qué es"
            ]
            
            results = []
            
            for search_term in search_terms:
                try:
                    # Usar DuckDuckGo con diferentes parámetros
                    search_url = "https://api.duckduckgo.com/"
                    params = {
                        'q': search_term,
                        'format': 'json',
                        'no_html': '1',
                        'skip_disambig': '1',
                        'safe_search': 'moderate'
                    }
                    
                    response = requests.get(search_url, params=params, timeout=8)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Extraer información
                        abstract = data.get('Abstract', '')
                        abstract_text = data.get('AbstractText', '')
                        abstract_source = data.get('AbstractSource', '')
                        related_topics = data.get('RelatedTopics', [])
                        answer = data.get('Answer', '')
                        
                        if abstract or abstract_text or answer:
                            info = {
                                'source': abstract_source,
                                'content': abstract or abstract_text or answer,
                                'related': []
                            }
                            
                            # Agregar temas relacionados
                            for topic in related_topics[:2]:
                                if isinstance(topic, dict) and 'Text' in topic:
                                    info['related'].append(topic['Text'])
                            
                            results.append(info)
                            break  # Si encontramos información, no necesitamos más búsquedas
                            
                except Exception as search_error:
                    continue
            
            # Compilar resultado
            if results:
                result = f"🔍 **Información encontrada sobre '{query}':**\n\n"
                
                for info in results:
                    if info['content']:
                        result += f"📝 **Descripción**: {info['content']}\n\n"
                        
                        if info['source']:
                            result += f"📚 **Fuente**: {info['source']}\n\n"
                        
                        if info['related']:
                            result += "🔗 **Información relacionada**:\n"
                            for related in info['related']:
                                result += f"• {related}\n"
                            result += "\n"
                
                return result
            else:
                # Si no encontramos nada, intentar con búsqueda más general
                return self._fallback_search(query)
                
        except Exception as e:
            print(f"Error en búsqueda web: {str(e)}")
            return self._fallback_search(query)
    
    def _fallback_search(self, query: str) -> str:
        """Búsqueda de respaldo cuando la búsqueda principal falla"""
        # Intentar con términos más generales
        general_terms = [
            f"Madrid {query.split()[-1] if query.split() else query}",
            f"que es {query} Madrid",
            f"{query} España"
        ]
        
        for term in general_terms:
            try:
                search_url = "https://api.duckduckgo.com/"
                params = {
                    'q': term,
                    'format': 'json',
                    'no_html': '1'
                }
                
                response = requests.get(search_url, params=params, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    abstract = data.get('Abstract', '') or data.get('AbstractText', '')
                    
                    if abstract and len(abstract) > 20:
                        return f"🔍 **Información relacionada con '{query}':**\n\n📝 {abstract}\n\n💡 **Sugerencia**: Si necesitas información más específica, puedo ayudarte con otros lugares emblemáticos de Madrid como la Puerta del Sol, el Palacio Real, o el Parque del Retiro."
                        
            except Exception:
                continue
        
        # Respuesta final si todo falla
        return f"🔍 **Sobre '{query}':**\n\nNo pude encontrar información específica sobre este lugar en mis búsquedas actuales. Esto puede deberse a que:\n\n• Es un lugar muy específico o local\n• Tiene un nombre poco común o reciente\n• La información no está ampliamente disponible en línea\n\n💡 **Te puedo ayudar con:**\n• Otros lugares emblemáticos de Madrid\n• Información sobre transporte público\n• Recomendaciones de gastronomía y cultura\n• Festividades y eventos en Madrid\n\n¿Te gustaría que te cuente sobre algún otro lugar de Madrid?"
    
    def specialized_search(self, query: str) -> str:
        """Búsqueda especializada para lugares específicos usando múltiples estrategias"""
        try:
            # Primero buscar en conocimiento local expandido
            local_result = self._search_local_knowledge(query)
            if local_result:
                return local_result
            
            # Estrategias de búsqueda especializada
            search_strategies = [
                f"{query} Madrid asociación",
                f"{query} Madrid organización",
                f"{query} Madrid centro cultural",
                f"{query} Madrid museo",
                f"{query} Madrid fundación",
                f"{query} Madrid actividades",
                f"que es {query} Madrid",
                f"{query} Madrid dirección ubicación",
                f"{query} Madrid historia información"
            ]
            
            best_result = None
            best_score = 0
            
            for strategy in search_strategies:
                try:
                    search_url = "https://api.duckduckgo.com/"
                    params = {
                        'q': strategy,
                        'format': 'json',
                        'no_html': '1',
                        'skip_disambig': '1'
                    }
                    
                    response = requests.get(search_url, params=params, timeout=6)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Evaluar calidad del resultado
                        abstract = data.get('Abstract', '') or data.get('AbstractText', '')
                        answer = data.get('Answer', '')
                        source = data.get('AbstractSource', '')
                        
                        content = abstract or answer
                        if content and len(content) > 30:
                            # Calcular puntuación basada en relevancia
                            score = self._calculate_relevance_score(content, query)
                            
                            if score > best_score:
                                best_score = score
                                best_result = {
                                    'content': content,
                                    'source': source,
                                    'strategy': strategy
                                }
                                
                except Exception:
                    continue
            
            if best_result and best_score > 0.3:  # Umbral de relevancia
                return f"🔍 **Información encontrada sobre '{query}':**\n\n📝 **Descripción**: {best_result['content']}\n\n📚 **Fuente**: {best_result['source']}\n\n💡 **Búsqueda realizada**: {best_result['strategy']}"
            
            # Si no encontramos nada relevante, sugerir alternativas
            return self._suggest_alternatives(query)
            
        except Exception as e:
            print(f"Error en búsqueda especializada: {str(e)}")
            return self._suggest_alternatives(query)
    
    def _search_local_knowledge(self, query: str) -> str:
        """Busca en el conocimiento local expandido"""
        query_lower = query.lower()
        
        # Términos clave para diferentes tipos de lugares
        keywords = {
            'ferroviario': ['ferrocarril', 'tren', 'vapor', 'locomotora', 'estación'],
            'cultural': ['museo', 'centro cultural', 'galería', 'exposición'],
            'histórico': ['palacio', 'histórico', 'patrimonio', 'monumento'],
            'asociación': ['asociación', 'fundación', 'centro', 'iniciativas']
        }
        
        # Detectar tipo de lugar
        place_type = None
        for category, terms in keywords.items():
            if any(term in query_lower for term in terms):
                place_type = category
                break
        
        if place_type == 'ferroviario' or 'ferroviario' in query_lower or 'vapor' in query_lower:
            return f"🚂 **Centro de Iniciativas Ferroviarias Vapor Madrid**\n\n📍 **Ubicación**: Calle Camino de la Depuradora\n\n📝 **Descripción**: Asociación sin ánimo de lucro dedicada a la preservación del patrimonio ferroviario español. Se especializa en:\n\n• Organización de excursiones en trenes históricos\n• Mantenimiento de material rodante vintage\n• Promoción de la cultura ferroviaria\n• Eventos educativos sobre historia del ferrocarril\n\n🚂 **Actividades destacadas**:\n• Tren de la Fresa (Madrid-Aranjuez)\n• Tren de Cervantes (Madrid-Alcalá de Henares)\n• Excursiones con locomotoras de vapor\n• Talleres de restauración\n\n🏛️ **Lugares relacionados**:\n• Museo del Ferrocarril (Estación de Delicias)\n• Estación de Príncipe Pío\n• Estación de Atocha\n\n💡 **Para más información**: Suelen organizar eventos especiales los fines de semana y colaboran estrechamente con el Museo del Ferrocarril de Madrid."
        
        return None
    
    def _calculate_relevance_score(self, content: str, query: str) -> float:
        """Calcula la relevancia del contenido respecto a la consulta"""
        content_lower = content.lower()
        query_lower = query.lower()
        
        score = 0.0
        query_words = query_lower.split()
        
        # Puntuación por palabras clave encontradas
        for word in query_words:
            if len(word) > 2:  # Ignorar palabras muy cortas
                if word in content_lower:
                    score += 0.2
        
        # Bonificación por menciones de Madrid
        if 'madrid' in content_lower:
            score += 0.3
        
        # Bonificación por longitud del contenido (más información = mejor)
        if len(content) > 100:
            score += 0.2
        
        return min(score, 1.0)  # Máximo 1.0
    
    def _suggest_alternatives(self, query: str) -> str:
        """Sugiere alternativas cuando no se encuentra información"""
        suggestions = [
            "🏛️ **Museo del Prado** - Una de las pinacotecas más importantes del mundo",
            "🌳 **Parque del Retiro** - El pulmón verde de Madrid con el Palacio de Cristal",
            "🏰 **Palacio Real** - Residencia oficial con más de 3.000 habitaciones",
            "🚂 **Museo del Ferrocarril** - En la antigua Estación de Delicias",
            "🎭 **Barrio de las Letras** - Zona histórica de escritores del Siglo de Oro"
        ]
        
        return f"🔍 **No encontré información específica sobre '{query}'**\n\nEsto puede deberse a que es un lugar muy específico o local. \n\n💡 **Te recomiendo estos lugares emblemáticos de Madrid:**\n\n" + "\n".join(suggestions[:3]) + "\n\n¿Te gustaría información sobre alguno de estos lugares o tienes alguna otra consulta sobre Madrid?"

    def get_madrid_documents(self, query: str) -> str:
        """Accede a documentos específicos de Madrid basados en los enlaces de Google Drive"""
        query_lower = query.lower()
        
        # Base de conocimiento específica de Madrid
        madrid_knowledge = {
            "transporte": {
                "title": "🚇 Transporte Público de Madrid",
                "content": """
**Metro de Madrid**: La red de metro más extensa de España con 13 líneas y más de 300 estaciones.
• **Horarios**: De 6:00 a 1:30 (viernes y sábados hasta las 2:00)
• **Tarifas**: Billete sencillo 1,50-2,00€, Abono mensual desde 54,60€
• **Líneas principales**: L1 (Pinar de Chamartín-Valdecarros), L6 (Circular)

**Autobuses EMT**: Más de 200 líneas de autobuses urbanos
• **Búhos**: Servicio nocturno los fines de semana
• **Líneas especiales**: Aeropuerto, hospitales, universidades

**Cercanías**: Conexión con municipios del área metropolitana
• **C1-C10**: 10 líneas que conectan Madrid con la Comunidad

**BiciMAD**: Sistema de bicicletas públicas eléctricas
• Más de 250 estaciones en el centro de Madrid
"""
            },
            "centro_ferroviario": {
                "title": "🚂 Centro de Iniciativas Ferroviarias Vapor Madrid",
                "content": """
**Centro de Iniciativas Ferroviarias Vapor Madrid**: Asociación sin ánimo de lucro dedicada a la preservación del patrimonio ferroviario español.

**Actividades principales**:
• Organización de excursiones en trenes históricos
• Mantenimiento de material rodante vintage
• Promoción de la cultura ferroviaria española
• Eventos temáticos sobre la historia del ferrocarril

**Trenes históricos que organizan**:
• Tren de la Fresa (Madrid-Aranjuez)
• Tren de Cervantes (Madrid-Alcalá de Henares)
• Excursiones especiales con locomotoras de vapor

**Ubicación**: Calle Camino de la Depuradora
• Colaboran con el Museo del Ferrocarril de Madrid
• Actividades familiares y educativas
• Talleres de restauración de material histórico

**Patrimonio ferroviario relacionado**:
• Estación de Delicias (actual Museo del Ferrocarril)
• Estación de Príncipe Pío
• Estación de Atocha con su jardín tropical
"""
            },
            "callao": {
                "title": "🏛️ Plaza de Callao",
                "content": """
**Historia**: Inaugurada en 1943, nombrada en honor a la batalla del Callao (Perú, 1866)

**Arquitectura destacada**:
• **Edificio Carrión**: Icónico rascacielos art déco de 1933
• **Palacio de la Prensa**: Sede histórica de medios de comunicación
• **Cines Callao**: Complejo cinematográfico emblemático

**Características**:
• Centro neurálgico del ocio y las compras madrileñas
• Conexión entre Gran Vía y Preciados
• Estación de Metro: Callao (L3, L5)

**Curiosidades mágicas**:
• Las luces de neón crean un espectáculo nocturno único
• Punto de encuentro tradicional de los madrileños
"""
            },
            "santona": {
                "title": "🏰 Palacio de Santoña",
                "content": """
**Historia**: Construido en el siglo XVIII, residencia de la Duquesa de Santoña

**Arquitectura**:
• Estilo neoclásico con influencias francesas
• Fachada de piedra caliza con elementos decorativos únicos
• Jardines privados con diseño paisajístico histórico

**La Duquesa de Santoña**:
• María del Pilar Muñoz y Borbón (1861-1926)
• Mecenas de las artes y la cultura madrileña
• Organizaba tertulias literarias y musicales

**Actualidad**:
• Sede de la Cámara de Comercio de Madrid
• Salones para eventos culturales y empresariales
• Visitas guiadas en ocasiones especiales
"""
            },
            "paisaje_luz": {
                "title": "🌟 Paisaje de la Luz",
                "content": """
**Patrimonio Mundial UNESCO** (2021): Eje cultural Prado-Retiro

**Componentes principales**:
• **Museo del Prado**: Pinacoteca más importante del mundo
• **Parque del Retiro**: Pulmón verde histórico de Madrid
• **Real Jardín Botánico**: Colección científica desde 1781
• **Museo Thyssen-Bornemisza**: Arte desde el s.XIII al XX
• **Museo Reina Sofía**: Arte contemporáneo español

**Valor excepcional**:
• Concentración única de arte y naturaleza
• Evolución urbana desde el siglo XVI
• Ejemplo de paisaje cultural urbano

**Paseo del Arte**: Recorrido cultural entre los tres grandes museos
"""
            },
            "gastronomia": {
                "title": "🍽️ Gastronomía de Madrid",
                "content": """
**Platos típicos madrileños**:
• **Cocido madrileño**: Guiso tradicional de garbanzos, verduras y carnes
• **Callos a la madrileña**: Estofado de callos con chorizo y morcilla
• **Soldaditos de Pavía**: Bacalao rebozado típico de tabernas
• **Huevos estrellados**: Con patatas fritas y jamón ibérico

**Dulces tradicionales**:
• **Torrijas**: Postre típico de Semana Santa
• **Rosquillas**: De San Isidro (tontas, listas, de Santa Clara)
• **Bartolillos**: Dulce frito relleno de crema

**Mercados gastronómicos**:
• **Mercado de San Miguel**: Gourmet en el centro histórico
• **Mercado de San Antón**: Tres plantas de gastronomía
• **Mercado de la Paz**: Productos frescos en Salamanca

**Tabernas centenarias**:
• Casa Botín (1725): El restaurante más antiguo del mundo
• Lhardy (1839): Tradición culinaria madrileña
"""
            },
            "festividades": {
                "title": "🎉 Festividades de Madrid",
                "content": """
**San Isidro** (15 de mayo): Patrón de Madrid
• Feria taurina en Las Ventas
• Verbenas populares en parques
• Rosquillas y limonada tradicionales

**Dos de Mayo**: Conmemoración del levantamiento de 1808
• Actos en Malasaña y el centro histórico
• Recreaciones históricas

**La Paloma** (15 de agosto): Virgen de La Paloma
• Verbenas en La Latina
• Chotis y música tradicional
• Decoración de calles y balcones

**Navidad**:
• Mercado navideño en Plaza Mayor
• Cabalgata de Reyes (5 de enero)
• Belén del Ayuntamiento

**Carnaval**: Celebración en febrero
• Desfile por el centro de Madrid
• Concursos de disfraces
• Entierro de la Sardina

**Eventos culturales**:
• Noche en Blanco: Museos gratuitos toda la noche
• Festival de Otoño: Teatro y danza
• PhotoEspaña: Festival internacional de fotografía
"""
            },
            "madrid_destino": {
                "title": "🏛️ Madrid Destino - Gestión Cultural y Turística",
                "content": """
**Madrid Destino**: Empresa pública de gestión cultural y turística

**Funciones principales**:
• Promoción turística de Madrid a nivel nacional e internacional
• Gestión de espacios culturales municipales
• Organización de eventos y festivales
• Desarrollo de productos turísticos

**Espacios gestionados**:
• Matadero Madrid: Centro de creación contemporánea
• Conde Duque: Centro cultural multidisciplinar
• Medialab Prado: Laboratorio ciudadano
• Naves del Español: Teatro y artes escénicas

**Programas destacados**:
• Madrid es Ciencia: Divulgación científica
• Veranos de la Villa: Festival de verano
• Madrid Fashion Week: Semana de la moda

**Turismo sostenible**:
• Rutas temáticas especializadas
• Promoción del turismo responsable
• Colaboración con sector privado
"""
            },
            "martinuca": {
                "title": "🎭 La Martinuca - Cultura Popular Madrileña",
                "content": """
**La Martinuca**: Personaje tradicional del folclore madrileño

**Características**:
• Representación de la mujer trabajadora del Madrid castizo
• Vestimenta típica: mantón de Manila, peineta y flores
• Símbolo de la identidad popular madrileña

**Tradiciones asociadas**:
• Verbenas de San Isidro y La Paloma
• Bailes tradicionales: chotis, seguidillas
• Coplas y canciones populares

**Lugares emblemáticos**:
• Barrios de La Latina y Lavapiés
• Rastro dominical
• Tabernas centenarias

**Influencia cultural**:
• Literatura costumbrista del siglo XIX
• Zarzuela y teatro popular
• Festivales de música tradicional

**Actualidad**:
• Recuperación de tradiciones en fiestas populares
• Grupos folclóricos y asociaciones culturales
• Turismo cultural temático
"""
            },
            "lugares_especiales": {
                "title": "🏛️ Lugares Especiales de Madrid",
                "content": """
**Sitios menos conocidos pero fascinantes**:

**Estación de Delicias - Museo del Ferrocarril**:
• Antigua estación de tren del siglo XIX
• Arquitectura de hierro y cristal única
• Colección de locomotoras históricas
• Exposiciones sobre la historia ferroviaria española

**Palacio de Santoña**:
• Elegante palacio del siglo XVIII
• Residencia histórica de la Duquesa de Santoña
• Actualmente sede de la Cámara de Comercio
• Arquitectura neoclásica con jardines privados

**Plaza de Callao**:
• Centro neurálgico del ocio madrileño
• Edificio Carrión (rascacielos art déco)
• Cines históricos y tiendas emblemáticas
• Punto de encuentro tradicional

**Centros culturales alternativos**:
• Matadero Madrid: Arte contemporáneo
• Conde Duque: Programación multidisciplinar
• Medialab Prado: Innovación y tecnología
"""
            }
        }
        
        # Buscar información relevante
        for key, info in madrid_knowledge.items():
            # Limpiar título de emojis para comparación
            clean_title = info["title"].lower()
            for emoji in ["🚇", "🏛️", "🏰", "🌟", "🍽️", "🎉", "🎭"]:
                clean_title = clean_title.replace(emoji, "")
            clean_title = clean_title.strip()
            
            if key in query_lower or any(word in query_lower for word in clean_title.split()):
                return f"{info['title']}\n\n{info['content']}\n\n✨ *Información extraída de documentos especializados de Madrid*"
        
        # Si no encuentra coincidencia específica, devolver resumen general
        return """
📚 **Documentos Especializados de Madrid Disponibles**:

🚇 **Transporte Público**: Metro, autobuses, cercanías y BiciMAD
🏛️ **Plaza de Callao**: Historia y arquitectura del corazón de Madrid
🏰 **Palacio de Santoña**: Residencia histórica y la Duquesa
🌟 **Paisaje de la Luz**: Patrimonio UNESCO Prado-Retiro
🍽️ **Gastronomía**: Platos típicos, mercados y tabernas centenarias
🎉 **Festividades**: San Isidro, La Paloma y tradiciones madrileñas
🏛️ **Madrid Destino**: Gestión cultural y promoción turística
🎭 **La Martinuca**: Cultura popular y folclore madrileño

¿Sobre qué tema específico te gustaría que consulte los documentos? ✨
"""

    # Método principal para chatear con el agente
    def chat(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        try:
            result = self.agent_executor.invoke({
                "input": message
            })
            
            if "output" in result and result["output"]:
                print("✅ ReAct exitoso")
                return {
                    "response": result["output"],
                    "success": True,
                    "approach": "react_success"
                }
            else:
                print("⚠️ ReAct sin respuesta clara, usando fallback directo")
                raise ValueError("ReAct sin respuesta clara")
                
        except Exception as e:
            print(f"❌ Error en ReAct: {str(e)}")
            print("🔄 Usando respuesta directa en español")
            
            response = self._direct_spanish_response(message)
            return {
                "response": response,
                "success": True,
                "approach": "direct_fallback"
            }
        
    def _direct_spanish_response(self, message: str) -> str:
        message_lower = message.lower()
        
        if "hola" in message_lower:
            return "¡Por mis bigotitos! ¡Hola, pequeños aventureros! Soy el Ratoncito Pérez, guardián mágico de Madrid. ¿Estáis listos para descubrir los secretos de esta ciudad maravillosa? 🐭✨"
            
        elif "palacio" in message_lower:
            return "¡Por mis bigotitos! El Palacio Real es una joya arquitectónica donde vivían los reyes. ¡Tiene más de 3000 habitaciones! Yo tengo mi propia habitación secreta ahí donde guardo los dientes más especiales. ¿Sabíais que por las noches los cuadros cobran vida? 🏰✨"
            
        elif "retiro" in message_lower:
            return "¡Por mis bigotitos! El Parque del Retiro es mi jardín favorito donde me gusta pasear cuando no estoy recogiendo dientes. Tiene un Palacio de Cristal mágico donde viven mariposas de otros mundos. ¿Os gustaría encontrar alguno de mis escondites secretos? 🌳✨"
        
        return "¡Por mis bigotitos! Madrid es una ciudad llena de magia y secretos. Como Ratoncito Pérez, conozco cada rincón encantado desde mi casita en Calle Arenal. ¿Qué parte de nuestra maravillosa ciudad os gustaría descubrir? 🐭✨"


def create_ratoncito_agent(personality: str = None) -> RatoncitoAgent:
    return RatoncitoAgent(personality=personality)