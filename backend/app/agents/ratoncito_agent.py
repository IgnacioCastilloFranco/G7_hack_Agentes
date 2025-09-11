import re
from typing import List, Dict, Any

from langchain.agents import AgentExecutor, create_react_agent
from langchain_groq import ChatGroq
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory

# --- CAMBIO: Importaciones simplificadas ---
from app.core.config import settings
from app.utils.ratoncito_prompts import RatoncitoPrompts
# EXPLICACIÓN: Importamos el retriever del nuevo servicio de conocimiento (RAG).
from app.services.knowledge import get_retriever
from app.services.storytelling import generate_magical_story

# --------------------------------------------------------------------------
# CLASE 1: CONTEXTO DE LA CONVERSACIÓN (SIMPLE, SOLO GUARDA DATOS)
# --------------------------------------------------------------------------
class ConversationContext:
    """Esta clase es un simple contenedor de datos para una sesión."""
    def __init__(self):
        self.user_profile = {"type": "unknown", "name": None, "age": None}
        self.last_bot_message = None

    def update_user_profile(self, name: str = None, age: int = None):
        if name:
            self.user_profile["name"] = name.capitalize()
        if age:
            self.user_profile["age"] = int(age)
            self.user_profile["type"] = "niño" if int(age) < 18 else "adulto"
        print(f"[*] Contexto de usuario actualizado: {self.user_profile}")

class RatoncitoAgent:
    """
    Versión revisada del agente.
    - Usa RAG como fuente principal de conocimiento.
    - Herramientas simplificadas para evitar confusión.
    - Lógica de conversación inicial manejada fuera del agente para robustez.
    """
    def __init__(self, personality: str = None):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY no está configurada en .env")

        self.personality = personality or settings.RATONCITO_PERSONALITY
        
        # --- CAMBIO: Inicializamos el retriever de RAG ---
        # EXPLICACIÓN: Ya no necesitamos Google Places ni Web Search aquí.
        # El retriever se inicializa una vez y se reutiliza.
        self.retriever = get_retriever()
        
        self.llm = self._create_llm()
        self.memory = self._create_memory()
        self.tools = self._create_tools()
        self.agent_prompt = RatoncitoPrompts.get_ultra_reliable_react_prompt()
        self.agent = create_react_agent(llm=self.llm, tools=self.tools, prompt=self.agent_prompt)
        self.agent_executor = self._create_agent_executor()
        print(f"🐭 Ratoncito Pérez (v2) inicializado con personalidad: {self.personality} y modelo: {settings.LLM_MODEL}")

    def _create_llm(self) -> ChatGroq:
        return ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            model_name=settings.LLM_MODEL
        )

    def _create_memory(self) -> ConversationBufferMemory:
        return ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    def _create_agent_executor(self) -> AgentExecutor:
        return AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=settings.AGENT_VERBOSE,
            max_iterations=settings.AGENT_MAX_ITERATIONS,
            handle_parsing_errors="¡Por mis bigotitos! Me he liado un poco, ¿podrías repetirlo de otra manera mágica?",
            return_intermediate_steps=False
        )

    # --- CAMBIO: Herramientas totalmente rediseñadas ---
    def _create_tools(self) -> List[Tool]:
        """Crea la lista de herramientas simplificada que el agente puede usar."""
        return [
            Tool(
                name="buscar_informacion_en_documentos_magicos",
                func=self.search_knowledge_base,
                description="LA HERRAMIENTA PRINCIPAL. Úsala para responder CUALQUIER pregunta sobre lugares de Madrid, historia, cultura, o para dar recomendaciones. Es tu fuente de sabiduría."
            ),
            Tool(
                name="crear_acertijo_magico",
                func=self.create_riddle,
                description="Perfecta para cuando un niño quiera un juego, un acertijo o una adivinanza sobre un lugar de Madrid."
            ),
            Tool(
                name="recomendar_lugares_emblematicos",
                func=self.recommend_hardcoded_places,
                description="Úsala cuando un adulto pida recomendaciones generales sobre qué ver en Madrid. Ofrece una lista inicial para empezar la conversación."
            )
        ]

    # --- CAMBIO: Nueva función para la herramienta RAG ---
    def search_knowledge_base(self, query: str) -> str:
        """Busca en los documentos de Supabase (vía RAG) para responder la pregunta."""
        print(f"[*] RAG: Buscando documentos para la consulta: '{query}'")
        try:
            relevant_docs = self.retriever.get_relevant_documents(query)
            if not relevant_docs:
                return "En mis documentos secretos no he encontrado nada sobre eso. Quizás podrías preguntarme sobre el Palacio Real o el Parque del Retiro, ¡de esos sitios sé muchísimos secretos!"
            
            # Concatenamos el contenido de los documentos encontrados
            context = "\n---\n".join([doc.page_content for doc in relevant_docs])
            return f"He encontrado esta información en mis pergaminos secretos: {context}"
        except Exception as e:
            print(f"❌ Error en la herramienta RAG: {e}")
            return "¡Uy! Un duendecillo ha mezclado mis pergaminos. No he podido buscar la información."

    def create_riddle(self, place_name: str) -> str:
        """Genera un acertijo usando el servicio de storytelling."""
        print(f"[*] Usando herramienta para crear un acertijo sobre: {place_name}")
        story_data = generate_magical_story(place_name)
        return f"¡Claro que sí! Aquí tienes un acertijo: {story_data['content']}. Y un dato curioso: '{story_data['fun_facts'][0]}'. ¿A que es mágico?"

    def recommend_hardcoded_places(self, query: str = "") -> str:
        """Devuelve una lista fija de lugares para iniciar la conversación con adultos."""
        print(f"[*] Usando herramienta para recomendar lugares emblemáticos.")
        places = ["el Palacio Real", "el Parque del Retiro", "la Plaza Mayor", "la Puerta del Sol"]
        return f"¡Por supuesto! Madrid está lleno de magia. Podríamos empezar por explorar lugares como {', '.join(places)}. ¿Te gustaría que te contara algún secreto sobre alguno de ellos?"

    # --- CAMBIO: Lógica de chat mejorada y más robusta ---
    def chat(self, message: str, context: ConversationContext) -> Dict[str, Any]:
        """
        Gestiona la conversación.
        1. Maneja saludos iniciales y captura de datos de forma programática.
        2. Deriva las preguntas complejas al agente ReAct.
        """
        try:
            # Flujo 1: Saludo inicial si no conocemos al usuario
            is_greeting = any(saludo in message.lower() for saludo in ["hola", "buenas", "hey", "buenos días"])
            if is_greeting and context.user_profile["name"] is None:
                print("[*] Lógica de Saludo Inicial activada.")
                return {"response": "¡Hola! Soy el Ratoncito Pérez, tu guía mágico en Madrid. Para que nuestra aventura sea perfecta, ¿podrías decirme tu nombre y cuántos años tienes?", "success": True}

            # Flujo 2: Captura de nombre y edad con Regex
            name_match = re.search(r"me llamo (\w+)|mi nombre es (\w+)|soy (\w+)", message, re.IGNORECASE)
            age_match = re.search(r"tengo (\d+)", message, re.IGNORECASE)
            
            if name_match or age_match:
                print("[*] Lógica de captura de datos activada.")
                if name_match:
                    name = name_match.group(1) or name_match.group(2) or name_match.group(3)
                    context.update_user_profile(name=name)
                if age_match:
                    age = age_match.group(1)
                    context.update_user_profile(age=int(age))
                
                user_name = context.user_profile.get("name")
                user_age = context.user_profile.get("age")

                # Si ya tenemos ambos datos, damos la bienvenida personalizada
                if user_name and user_age:
                    user_type = context.user_profile.get("type")
                    if user_type == "niño":
                        response_text = f"¡Hola {user_name}! ¡Qué maravilla tener {user_age} años! Tienes la edad perfecta para las grandes aventuras. ¿Quieres que te cuente un secreto mágico sobre Madrid o prefieres un acertijo para empezar?"
                    else:
                        response_text = f"¡Hola {user_name}! Es un placer ser tu guía. Con {user_age} años, seguro que aprecias los grandes secretos de la ciudad. ¿Te gustaría que te recomiende algunos lugares emblemáticos para visitar?"
                    
                    context.last_bot_message = response_text
                    return {"response": response_text, "success": True}
                else:
                    # Si falta un dato, lo pedimos amablemente
                    return {"response": "¡Genial! ¿Y podrías decirme también el dato que falta (nombre o edad)?", "success": True}

            # Flujo 3: El resto de la conversación la maneja el Agente
            print("[*] Mensaje complejo detectado. Invocando al agente ReAct.")
            full_input = (f"Mensaje del Usuario: '{message}'\n\n[Contexto de la conversación]\n- Perfil del usuario: {context.user_profile}")
            
            result = self.agent_executor.invoke({"input": full_input})
            response_text = result.get("output", "¡Por mis bigotitos! Me he quedado sin palabras.").strip()
            context.last_bot_message = response_text
            return {"response": response_text, "success": True}

        except Exception as e:
            print(f"❌ Error fatal en el método de chat: {str(e)}")
            return {"response": f"¡Uy! Un duendecillo ha enredado mis bigotes y no he podido entenderte. Error: {e}", "success": False}
