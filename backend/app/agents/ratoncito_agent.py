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
        """Realiza una búsqueda web para obtener información actualizada"""
        try:
            # Usar DuckDuckGo como motor de búsqueda gratuito
            search_url = "https://api.duckduckgo.com/"
            params = {
                'q': f"{query} Madrid",
                'format': 'json',
                'no_html': '1',
                'skip_disambig': '1'
            }
            
            response = requests.get(search_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extraer información relevante
                abstract = data.get('Abstract', '')
                related_topics = data.get('RelatedTopics', [])
                
                result = f"🔍 **Información encontrada sobre '{query}':**\n\n"
                
                if abstract:
                    result += f"📝 **Resumen**: {abstract}\n\n"
                
                if related_topics:
                    result += "🔗 **Temas relacionados**:\n"
                    for i, topic in enumerate(related_topics[:3]):  # Limitar a 3 resultados
                        if isinstance(topic, dict) and 'Text' in topic:
                            result += f"• {topic['Text']}\n"
                
                if not abstract and not related_topics:
                    result += "No encontré información específica, pero puedo ayudarte con mis conocimientos sobre Madrid. ¿Hay algo más específico que te gustaría saber?"
                
                return result
            else:
                return "🔍 No pude realizar la búsqueda en este momento. ¿Puedo ayudarte con mis conocimientos sobre Madrid?"
                
        except Exception as e:
             print(f"Error en búsqueda web: {str(e)}")
             return "🔍 Hubo un problema con la búsqueda web, pero puedo ayudarte con mis conocimientos sobre Madrid. ¿Qué te gustaría saber?"

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