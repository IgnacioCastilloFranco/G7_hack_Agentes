from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from typing import Dict, Any, List
import random
import re
from app.core.config import settings

class MagicRatoncitoAgent:
    def __init__(self, personality: str = None):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY no está configurada en .env")

        self.personality = personality or settings.RATONCITO_PERSONALITY
        self.llm = self._create_llm()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Base de conocimiento mágica
        self.madrid_knowledge = self._load_madrid_knowledge()
        self.magical_greetings = self._load_magical_greetings()
        
        print(f"🐭 Ratoncito Pérez MÁGICO inicializado: {self.personality}")
        print(f"🧠 Modelo: {settings.LLM_MODEL}")

    def _create_llm(self) -> ChatGroq:
        return ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            model_name=settings.LLM_MODEL
        )

    def _load_madrid_knowledge(self) -> Dict[str, str]:
        """Conocimiento mágico de Madrid"""
        return {
            "palacio real": "¡Por mis bigotitos! El Palacio Real es una joya arquitectónica donde vivían los reyes. ¡Tiene más de 3000 habitaciones! Yo tengo mi propia habitación secreta ahí donde guardo los dientes más especiales que me dais... 🏰 ¿Sabéis que por las noches los cuadros cobran vida y bailan conmigo?",
            
            "plaza mayor": "¡Qué mágica! La Plaza Mayor es el corazón de Madrid, donde se celebraban fiestas y mercados. ¡He visto tantas celebraciones desde mis escondites en los balcones! Por las noches de luna llena, todos los ratones bajamos y organizamos bailes secretos... 🎉 ¡Os invito alguna vez!",
            
            "retiro": "¡Mi jardín favorito! El Parque del Retiro es donde me gusta pasear cuando no estoy recogiendo dientes. Tiene un Palacio de Cristal mágico donde viven mariposas de otros mundos, y muchos árboles centenarios donde escondo sorpresas para los niños más buenos... 🌳 ¿Os gustaría encontrar alguna?",
            
            "puerta del sol": "¡El centro de toda España! La Puerta del Sol es donde está el kilómetro 0, desde aquí se miden todas las distancias del país. Yo tengo túneles secretos que conectan con todas las calles de Madrid... ⭐ ¡Por mis bigotitos, qué aventuras he vivido corriendo por ahí!",
            
            "calle arenal": "¡Mi hogar dulce hogar! En la Calle Arenal número 8 tengo mi casita muy especial. Ahí es donde guardo todos los dientes de leche más preciados y donde escribo las historias mágicas de todos los niños de Madrid... 🏠 ¿Os gustaría visitarla algún día?",
            
            "prado": "¡El museo más mágico! En el Prado viven las pinturas más hermosas del mundo. Por las noches, cuando no hay visitantes, los personajes de los cuadros cobran vida y charlamos sobre arte... 🎨 Las Meninas son muy buenas amigas mías.",
            
            "reina sofía": "¡Un museo moderno lleno de sorpresas! El Reina Sofía guarda el Guernica de Picasso. A mí me gusta mucho porque los cuadros modernos tienen formas divertidas donde puedo esconderme... 🎭",
            
            "templo debod": "¡Un templo egipcio en Madrid! El Templo de Debod viajó desde muy lejos, como yo cuando vine de otros países para vivir aquí. Por las noches brilla de forma mágica... 🌙"
        }

    def _load_magical_greetings(self) -> List[str]:
        """Saludos mágicos variados"""
        return [
            "¡Por mis bigotitos! ¡Hola, pequeños aventureros! 🐭✨ Soy el Ratoncito Pérez y vivo en la Calle Arenal. Estoy aquí para mostraros los secretos mágicos de Madrid. ¿Estáis listos para una aventura increíble?",
            
            "¡Qué aventureros tan curiosos! ¡Bienvenidos a mi mundo mágico! 🎭 Soy el guardián de las historias más fantásticas de Madrid. Desde mi casita en Calle Arenal conozco todos los rincones encantados. ¿Me acompañáis en esta aventura?",
            
            "¡Secretos mágicos os esperan! 🏰 Soy el Ratoncito Pérez, y después de siglos viviendo en Madrid, conozco cada rincón encantado de esta hermosa ciudad. ¿Qué lugar os gustaría explorar primero?",
            
            "¡Una aventura nos espera! 🌟 ¡Hola! Soy vuestro ratoncito favorito, el mismísimo Ratoncito Pérez. Madrid es mi hogar y está lleno de magia que solo yo puedo mostraros. ¿Estáis preparados para descubrir sus secretos?"
        ]

    def _detect_intent(self, message: str) -> str:
        """Detectar la intención del mensaje"""
        message_lower = message.lower()
        
        # Saludos
        greetings = ["hola", "buenos días", "buenas tardes", "buenas noches", "hey", "saludos", "hi", "hello"]
        if any(greeting in message_lower for greeting in greetings):
            return "greeting"
        
        # Lugares de Madrid
        madrid_places = list(self.madrid_knowledge.keys())
        for place in madrid_places:
            if place in message_lower:
                return f"madrid_info:{place}"
        
        # Preguntas generales sobre Madrid
        madrid_keywords = ["madrid", "ciudad", "lugar", "visitar", "conocer", "turismo", "pasear"]
        if any(keyword in message_lower for keyword in madrid_keywords):
            return "general_madrid"
            
        # Preguntas sobre el Ratoncito Pérez
        ratoncito_keywords = ["ratoncito", "pérez", "dientes", "casa", "vives", "eres"]
        if any(keyword in message_lower for keyword in ratoncito_keywords):
            return "about_ratoncito"
        
        return "general_chat"

    def _get_greeting_response(self) -> str:
        return random.choice(self.magical_greetings)

    def _get_madrid_info_response(self, place: str) -> str:
        return self.madrid_knowledge.get(place, self._get_unknown_place_response(place))

    def _get_unknown_place_response(self, place: str) -> str:
        return f"¡Qué lugar tan curioso mencionáis! '{place}' suena interesante, pero no tengo información mágica específica sobre ese sitio. Sin embargo, puedo contaros maravillas del Palacio Real, Plaza Mayor, Retiro, o mi casita en Calle Arenal. ¿Cuál os llama más la atención? 🐭✨"

    def _get_llm_response(self, message: str, intent: str) -> str:
        
        # Preparar contexto según la intención
        if intent == "general_madrid":
            context = "El usuario pregunta sobre Madrid en general. Recomienda lugares mágicos."
        elif intent == "about_ratoncito":
            context = "El usuario pregunta sobre ti, el Ratoncito Pérez. Habla de tu vida en Calle Arenal."
        else:
            context = "Responde de manera mágica y entrañable."

        # Obtener historial reciente
        recent_history = ""
        if self.memory.chat_memory.messages:
            for msg in self.memory.chat_memory.messages[-4:]:
                if hasattr(msg, 'content'):
                    recent_history += f"- {msg.content[:100]}...\n"

        prompt = PromptTemplate.from_template("""
Eres el Ratoncito Pérez, guardián mágico de Madrid que vive en Calle Arenal número 8.

TU PERSONALIDAD:
- Mágico, entrañable y lleno de asombro
- Usas expresiones: ¡Por mis bigotitos!, ¡Qué aventureros!, ¡Secretos mágicos!
- Hablas usando español de España.
- Mezclas información real con fantasía mágica
- Siempre positivo y acogedor

CONTEXTO: {context}

CONVERSACIÓN RECIENTE:
{recent_history}

PREGUNTA DEL USUARIO: {message}

Responde como el Ratoncito Pérez de manera mágica, breve y entrañable (máximo 3 frases):""")

        try:
            formatted_prompt = prompt.format(
                context=context,
                recent_history=recent_history,
                message=message
            )
            
            response = self.llm.invoke(formatted_prompt)
            return response.content
            
        except Exception as e:
            return f"¡Por mis bigotitos! Algo mágico inesperado pasó... Pero no os preocupéis, ¡siempre estoy aquí para ayudaros! 🐭✨"

    def chat(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        try:
            intent = self._detect_intent(message)
            
            if intent == "greeting":
                response = self._get_greeting_response()
                response_type = "greeting"
                
            elif intent.startswith("madrid_info:"):
                place = intent.split(":")[1]
                response = self._get_madrid_info_response(place)
                response_type = "madrid_info"
                
            else:
                response = self._get_llm_response(message, intent)
                response_type = "llm_response"
            
            self.memory.save_context(
                {"input": message},
                {"output": response}
            )
            
            return {
                "response": response,
                "success": True,
                "type": response_type,
                "intent": intent,
                "model_used": settings.LLM_MODEL,
                "personality": self.personality
            }

        except Exception as e:
            return {
                "response": f"¡Por mis bigotitos! Algo mágico inesperado pasó, pero no os preocupéis. Siempre estoy aquí para ayudaros con los secretos de Madrid. 🐭✨",
                "success": False,
                "error": str(e)
            }

    def reset_conversation(self):
        self.memory.clear()
        print("🧠 Memoria mágica del Ratoncito Pérez reiniciada")

def create_magic_ratoncito_agent(personality: str = None) -> MagicRatoncitoAgent:
    return MagicRatoncitoAgent(personality=personality)