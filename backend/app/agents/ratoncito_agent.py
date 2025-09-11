import re
import random
from typing import List, Dict, Any

from langchain.agents import AgentExecutor, create_react_agent
from langchain_groq import ChatGroq
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory

from app.core.config import settings
from app.utils.ratoncito_prompts import RatoncitoPrompts
from app.services.knowledge import get_retriever
from app.services.riddles import get_riddle_for_place 
from app.services.tourism import search_madrid_data, format_results_for_agent

class ConversationContext:
    def __init__(self):
        self.user_profile = {"type": "unknown", "name": None, "age": None}

    def update_user_profile(self, name: str = None, age: int = None):
        if name:
            self.user_profile["name"] = name.capitalize()
        if age:
            self.user_profile["age"] = int(age)
            self.user_profile["type"] = "niño" if int(age) < 18 else "adulto"
        print(f"[*] Contexto de usuario actualizado: {self.user_profile}")

class RatoncitoAgent:
    def __init__(self, personality: str = None):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY no está configurada en .env")

        self.personality = personality or settings.RATONCITO_PERSONALITY
        self.retriever = get_retriever()
        
        self.llm = self._create_llm()
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.tools = self._create_tools()
        self.agent_prompt = RatoncitoPrompts.get_ultra_reliable_react_prompt()
        self.agent = create_react_agent(llm=self.llm, tools=self.tools, prompt=self.agent_prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=settings.AGENT_VERBOSE,
            max_iterations=settings.AGENT_MAX_ITERATIONS,
            handle_parsing_errors="¡Por mis bigotitos! Me he liado un poco, ¿podrías repetirlo de otra manera mágica?",
        )
        print(f"🐭 Ratoncito Pérez (v3) inicializado con personalidad: {self.personality} y modelo: {settings.LLM_MODEL}")

    def _create_llm(self) -> ChatGroq:
        return ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            model_name=settings.LLM_MODEL
        )

    def _create_tools(self) -> List[Tool]:
        return [
            Tool(
                name="buscar_informacion_en_documentos_magicos",
                func=self.search_knowledge_base,
                description="LA HERRAMIENTA PRINCIPAL. Úsala para responder CUALQUIER pregunta sobre lugares de Madrid, historia, cultura, o para dar recomendaciones. Es tu fuente de sabiduría."
            ),
            Tool(
                name="consultar_datos_oficiales_madrid",
                func=self.query_madrid_open_data,
                description="Consulta las APIs y archivos JSON oficiales de Madrid para encontrar información específica sobre eventos, transporte o servicios."
            ),
            Tool(
                name="crear_acertijo_magico",
                func=self.create_riddle,
                description="Perfecta para cuando un niño quiera un juego o un acertijo sobre un lugar de Madrid."
            ),
            Tool(
                name="recomendar_lugares_emblematicos",
                func=self.recommend_hardcoded_places,
                description="Úsala como último recurso si un adulto pide recomendaciones generales y no encuentras nada en los documentos."
            )
        ]

    def search_knowledge_base(self, query: str) -> str:
        print(f"[*] RAG: Buscando documentos para la consulta: '{query}'")
        relevant_docs = self.retriever.get_relevant_documents(query)
        if not relevant_docs:
            return "En mis documentos secretos no he encontrado nada sobre eso."
        context = "\n---\n".join([doc.page_content for doc in relevant_docs])
        return f"He encontrado esta información en mis pergaminos secretos: {context}"

    def query_madrid_open_data(self, query: str) -> str:
        print(f"[*] Consultando datos abiertos de Madrid para: '{query}'")
        items = search_madrid_data(query)
        return format_results_for_agent(items)

    def create_riddle(self, place_name: str) -> str:
        print(f"[*] Creando un acertijo sobre: {place_name}")
        riddle = get_riddle_for_place(place_name)
        return f"¡Claro que sí! Aquí tienes un acertijo mágico: {riddle}"

    def recommend_hardcoded_places(self, query: str = "") -> str:
        places = ["el Palacio Real", "el Parque del Retiro", "la Plaza Mayor"]
        return f"¡Por supuesto! Madrid está lleno de magia. Podríamos empezar por {', '.join(places)}. ¿Quieres que te cuente un secreto sobre alguno?"

    def chat(self, message: str, context: ConversationContext) -> Dict[str, Any]:
        try:
            despedidas = ["adiós", "adios", "hasta luego", "chao", "me voy"]
            if any(despedida in message.lower() for despedida in despedidas):
                user_name = context.user_profile.get("name", "aventurero")
                return {"response": f"¡Ha sido un placer, {user_name}! ¡Hasta la próxima aventura!", "success": True}
            
            is_greeting = any(saludo in message.lower() for saludo in ["hola", "buenas"])
            if is_greeting and context.user_profile.get("name") is None:
                return {"response": "¡Hola! Soy el Ratoncito Pérez. Para que nuestra aventura sea perfecta, dime tu nombre y cuántos años tienes.", "success": True}

            name_match = re.search(r"me llamo (\w+)|mi nombre es (\w+)|soy (\w+)", message, re.IGNORECASE)
            age_match = re.search(r"tengo (\d+)", message, re.IGNORECASE)
            
            if name_match or age_match:
                if name_match: context.update_user_profile(name=(name_match.group(1) or name_match.group(2) or name_match.group(3)))
                if age_match: context.update_user_profile(age=int(age_match.group(1)))
                
                user_name = context.user_profile.get("name")
                user_age = context.user_profile.get("age")

                if user_name and user_age:
                    user_type = context.user_profile.get("type")
                    if user_type == "niño":
                        return {"response": f"¡Hola {user_name}! ¡Qué maravilla tener {user_age} años! ¿Quieres que te cuente un secreto o prefieres un acertijo para empezar?", "success": True}
                    else:
                        return {"response": f"¡Hola {user_name}! Con {user_age} años, seguro que aprecias los secretos de la ciudad. ¿Sobre qué lugar te gustaría saber más?", "success": True}
                else:
                    return {"response": "¡Genial! ¿Y el dato que falta (nombre o edad)?", "success": True}

            print("[*] Mensaje complejo detectado. Invocando al agente ReAct.")
            full_input = (f"Mensaje del Usuario: '{message}'\n[Contexto]\n- Perfil: {context.user_profile}")
            
            result = self.agent_executor.invoke({"input": full_input})
            return {"response": result.get("output", "¡Por mis bigotitos! Algo ha salido mal.").strip(), "success": True}

        except Exception as e:
            print(f"❌ Error fatal en el chat: {e}")
            return {"response": "¡Uy! Un duendecillo ha enredado mis bigotes.", "success": False}