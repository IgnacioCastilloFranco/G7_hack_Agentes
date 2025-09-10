from langchain.agents import AgentExecutor, create_react_agent
from langchain_groq import ChatGroq
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from typing import List, Dict, Any
import os
from app.core.config import settings
from app.utils.ratoncito_prompts import RatoncitoPrompts
from app.services.knowledge import get_retriever
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
        self.retriever = get_retriever()
        self.tools = self.create_tools()
        self.agent = self.create_agent()
        self.agent_executor = self.create_agent_executor()

        print(f"🐭 Ratoncito Pérez inicializado con personalidad: {self.personality}")
        print(f"🧠 Modelo: {settings.LLM_MODEL}")
        print(f"📦 Retriever activo: {type(self.retriever).__name__}")

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
                name="buscar_conocimiento",
                description="Buscar en la base de conocimiento (PDFs del bucket) para responder preguntas.",
                func=self.search_knowledge
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
            early_stopping_method="force",  
            return_intermediate_steps=False,
            max_execution_time=settings.AGENT_MAX_EXECUTION_SECONDS
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

    def search_knowledge(self, query: str) -> str:
        try:
            # Use new retriever API when available
            if hasattr(self.retriever, "invoke"):
                docs = self.retriever.invoke(query)
            else:
                docs = self.retriever.get_relevant_documents(query)
        except Exception as e:
            return f"Error al buscar en la base de conocimiento: {str(e)}"

        print(f"🔍 Buscando en la base de conocimiento: {query}")
        print(f"📄 numero de Documentos encontrados: {len(docs)}")
        print(f"📄 Documentos encontrados: {docs}")
        if not docs:
            return "No encontré información relevante en los PDFs."

        snippets: List[str] = []
        for d in docs:
            text = (getattr(d, "page_content", "") or "").strip()
            if text:
                snippets.append(text[:600])
            if len(snippets) >= 4:
                break
        if not snippets:
            return "No encontré contenido útil en los documentos recuperados."
        return "\n\n".join(snippets)


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