from langchain.agents import AgentExecutor, create_react_agent
from langchain_groq import ChatGroq
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from typing import List, Dict, Any
from duckduckgo_search import DDGS
from app.core.config import settings
from app.utils.ratoncito_prompts import RatoncitoPrompts

class ConversationContext:
    def __init__(self):
        self.user_profile = {"type": "unknown", "name": None, "age": None}
        self.current_location_context = None

    def update_user(self, user_type="unknown", name=None, age=None):
        self.user_profile["type"] = user_type
        self.user_profile["name"] = name if name else self.user_profile["name"]
        self.user_profile["age"] = age if age else self.user_profile["age"]
        print(f"[*] Contexto de usuario actualizado: {self.user_profile}")

    def set_location(self, location):
        self.current_location_context = location
        print(f"[*] Contexto de lugar actualizado: {self.current_location_context}")

# Creamos una instancia global del contexto para que persista entre llamadas
conversation_context = ConversationContext()

class RatoncitoAgent:
    def __init__(self, personality: str = None):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY no está configurada en .env")

        self.personality = personality or settings.RATONCITO_PERSONALITY
        self.llm = self._create_llm()
        self.memory = self._create_memory()
        self.tools = self._create_tools()
        self.agent_prompt = RatoncitoPrompts.get_ultra_reliable_react_prompt()
        self.agent = create_react_agent(llm=self.llm, tools=self.tools, prompt=self.agent_prompt)
        self.agent_executor = self._create_agent_executor()

        print(f"🐭 Ratoncito Pérez inicializado con personalidad: {self.personality} y modelo: {settings.LLM_MODEL}")

    def _create_llm(self) -> ChatGroq:
        return ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            model_name=settings.LLM_MODEL
        )

    def _create_memory(self) -> ConversationBufferMemory:
        return ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    def _create_tools(self) -> List[Tool]:
        return [
            Tool(
                name="identificar_usuario_y_saludar",
                func=self.identify_user_and_greet,
                description="Usar SIEMPRE al principio de la conversación para saludar y determinar si el usuario es un niño o un adulto."
            ),
            Tool(
                name="informacion_lugar_madrid",
                func=self.madrid_info,
                description="Proporciona información mágica sobre lugares icónicos de Madrid. Úsalo si te preguntan por un lugar específico."
            ),
            Tool(
                name="ofrecer_actividad_magica",
                func=self.offer_magical_activity,
                description="Crea un acertijo o dato curioso sobre un lugar. Perfecto para interactuar con niños."
            ),
            Tool(
                name="recomendar_plan_familiar",
                func=self.recommend_family_plan,
                description="Recomienda lugares o actividades en Madrid para familias. Ideal para peticiones de adultos."
            ),
            Tool(
                name="busqueda_web_general",
                func=self.web_search,
                description="Busca en la web información específica que no se encuentra en las otras herramientas. Usar como último recurso."
            ),
            Tool(
                name="recordar_lugar_actual",
                func=self.remember_current_location,
                description="Actualiza el lugar del que se está hablando. Se usa cuando se menciona un nuevo lugar para guardarlo en contexto."
            )
        ]

    def _create_agent_executor(self) -> AgentExecutor:
        return AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=settings.AGENT_VERBOSE,
            max_iterations=settings.AGENT_MAX_ITERATIONS,
            handle_parsing_errors="¡Por mis bigotitos! Me he liado un poco, ¿podrías repetirlo de otra manera mágica?",
            early_stopping_method="force"
        )

    def identify_user_and_greet(self, input_text: str) -> str:
        """
        Esta herramienta ahora devuelve un DATO, no una instrucción.
        Esto evita que el agente entre en bucle.
        """
        input_lower = input_text.lower()
        if "niño" in input_lower or "peque" in input_lower or "hijo" in input_lower:
            conversation_context.update_user(user_type="child")
            return "Dato para el agente: El usuario es un niño."
        elif "familia" in input_lower or "adulto" in input_lower or "padre" in input_lower or "madre" in input_lower:
            conversation_context.update_user(user_type="adult")
            return "Dato para el agente: El usuario es un adulto."
        
        conversation_context.update_user(user_type="unknown")
        return "Dato para el agente: Tipo de usuario desconocido."

    def madrid_info(self, place: str) -> str:
        current_place = place.lower().strip() if place else conversation_context.current_location_context
        if not current_place:
            return "No se ha especificado ningún lugar. Pregúntale al usuario sobre qué lugar de Madrid quiere saber."
        places = {
            "palacio real": "¡El Palacio Real es gigantesco! Tiene más de 3000 habitaciones. Yo tengo una secreta donde guardo los dientes de los príncipes y princesas. Por la noche, ¡las armaduras hacen carreras por los pasillos!",
            "plaza mayor": "La Plaza Mayor es como un gran patio de juegos. Antiguamente veían torneos de caballeros. Ahora, en Navidad, se llena de luces y puestos mágicos. ¡Es uno de mis sitios favoritos para deslizarme por los tejados!",
            "retiro": "¡El Retiro es mi jardín secreto! El Palacio de Cristal está hecho con burbujas de jabón gigantes que nunca explotan. Y en el estanque, los barquitos son empujados por peces de colores que me cuentan secretos del fondo del lago.",
            "puerta del sol": "Aquí está el Kilómetro Cero, ¡el ombligo de España! Desde mi casa en la Calle Arenal, tengo un túnel que llega justo debajo del Oso y el Madroño. Es mi atajo para recorrer la ciudad."
        }
        conversation_context.set_location(current_place)
        return places.get(current_place, f"No tengo un cuento mágico sobre '{current_place}', pero seguro que podemos buscar información fascinante. O si quieres, te cuento sobre el Palacio Real.")

    def offer_magical_activity(self, place: str) -> str:
        current_place = place.lower().strip() if place else conversation_context.current_location_context
        if not current_place:
             return "No hay un lugar seleccionado. No puedo crear una actividad."
        riddles = {
            "palacio real": "Tengo miles de ventanas pero no soy el cielo, reyes y reinas vivieron en mi suelo. ¿Qué soy? ... ¡El Palacio Real!",
            "retiro": "Tengo un palacio de cristal que no se rompe y un estanque donde el rey descansa en bronce. ¿Qué soy? ... ¡El Parque del Retiro!"
        }
        activity = riddles.get(current_place, f"Dato curioso de {current_place.title()}: ¡Los fantasmas de los artistas que vivieron allí a veces terminan los cuadros por la noche!")
        return f"¡Claro! Tengo un acertijo para ti sobre {current_place.title()}: {activity}"

    def recommend_family_plan(self, query: str) -> str:
        plans = [
            "Visitar el Museo del Ferrocarril en la estación de Delicias, ¡es un viaje en el tiempo!",
            "Dar un paseo en barca por el estanque del Retiro y luego buscar el Palacio de Cristal.",
            "Explorar el Templo de Debod al atardecer, ¡las vistas son mágicas!",
            "Perderse por el Madrid de los Austrias y acabar comiendo chocolate con churros en San Ginés."
        ]
        return f"¡Por supuesto! Para una aventura en familia por Madrid, os sugiero estos planes mágicos: {', '.join(plans)}. ¿Queréis que os cuente más sobre alguno?"

    def web_search(self, query: str) -> str:
        try:
            with DDGS() as ddgs:
                results = [r for r in ddgs.text(query, region='es-es', max_results=3)]
            if not results:
                return f"No encontré nada en mi bola de cristal sobre '{query}'."
            snippets = [f"{r.get('title', '')}: {r.get('body', '')}" for r in results]
            return "He consultado a los duendes de la información y me han contado esto: " + " | ".join(snippets)
        except Exception as e:
            return f"¡Mis bigotitos! Hubo un problema mágico al buscar. Error: {str(e)}"

    def remember_current_location(self, location: str) -> str:
        conversation_context.set_location(location.lower().strip())
        return f"Contexto actualizado. Ahora estamos hablando de {location}."

    def chat(self, message: str) -> Dict[str, Any]:
        try:
            full_input = f"""
Mensaje del usuario: "{message}"

[Contexto de la conversación actual para tu conocimiento]
- Perfil del usuario: {conversation_context.user_profile}
- Último lugar mencionado: {conversation_context.current_location_context or 'Ninguno'}
"""
            result = self.agent_executor.invoke({"input": full_input})
            
            response = result.get("output", "¡Por mis bigotitos! Me he quedado sin palabras mágicas. ¿Pregúntame otra cosa?").strip()
            return {"response": response, "success": True}
        except Exception as e:
            print(f"❌ Error en el agente ReAct: {str(e)}")
            return {"response": "¡Uy! Un duendecillo travieso ha enredado mis bigotes y no he podido procesar tu petición. ¿Podrías preguntármelo de otra forma?", "success": False, "error": str(e)}
