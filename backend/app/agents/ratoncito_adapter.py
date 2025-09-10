from typing import Dict, Any
from app.agents.multi_agent_system import create_madrid_multi_agent_system, MadridMultiAgentSystem
from app.agents.ratoncito_agent import RatoncitoAgent
from app.core.config import settings


class RatoncitoAgentAdapter:
    """Adaptador que permite usar el sistema multi-agente manteniendo la interfaz original"""
    
    def __init__(self, personality: str = None, use_multi_agent: bool = True):
        self.personality = personality or settings.RATONCITO_PERSONALITY
        self.use_multi_agent = use_multi_agent
        
        if self.use_multi_agent:
            print("🔄 Inicializando sistema multi-agente...")
            self.agent_system = create_madrid_multi_agent_system(self.personality)
            self.legacy_agent = None
        else:
            print("🔄 Inicializando agente legacy...")
            self.agent_system = None
            self.legacy_agent = RatoncitoAgent(self.personality)
    
    def chat(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Método principal de chat que mantiene la interfaz original"""
        try:
            if self.use_multi_agent:
                return self._chat_multi_agent(message, context)
            else:
                return self._chat_legacy(message, context)
                
        except Exception as e:
            print(f"❌ Error en adaptador: {str(e)}")
            return {
                "response": "¡Por mis bigotitos! Parece que tengo un pequeño problema técnico. ¿Podrías intentar preguntarme de nuevo? 🐭✨",
                "success": True,
                "approach": "error_fallback"
            }
    
    def _chat_multi_agent(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Procesa el chat usando el sistema multi-agente"""
        result = self.agent_system.process_query(message, context)
        
        # Adaptar la respuesta al formato esperado por la API
        return {
            "response": result['response'],
            "success": result['success'],
            "approach": result['approach'],
            "agents_used": result.get('agents_used', []),
            "context_info": result.get('context_info', {}),
            "system_type": "multi_agent"
        }
    
    def _chat_legacy(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Procesa el chat usando el agente legacy"""
        result = self.legacy_agent.chat(message, context)
        result["system_type"] = "legacy"
        return result
    
    def get_system_info(self) -> Dict[str, Any]:
        """Obtiene información del sistema actual"""
        if self.use_multi_agent:
            status = self.agent_system.get_system_status()
            return {
                "system_type": "multi_agent",
                "personality": self.personality,
                "agents_count": status['total_agents'],
                "agents": list(status['agents'].keys()),
                "current_context": status['current_context'],
                "conversation_history_length": status['conversation_history_length']
            }
        else:
            return {
                "system_type": "legacy",
                "personality": self.personality,
                "current_context": getattr(self.legacy_agent, 'current_site_context', None)
            }
    
    def switch_system(self, use_multi_agent: bool) -> Dict[str, str]:
        """Permite cambiar entre sistema multi-agente y legacy"""
        if use_multi_agent == self.use_multi_agent:
            return {
                "status": "no_change",
                "message": f"Ya estás usando el sistema {'multi-agente' if use_multi_agent else 'legacy'}"
            }
        
        try:
            self.use_multi_agent = use_multi_agent
            
            if self.use_multi_agent:
                self.agent_system = create_madrid_multi_agent_system(self.personality)
                self.legacy_agent = None
                return {
                    "status": "success",
                    "message": "Cambiado a sistema multi-agente"
                }
            else:
                self.legacy_agent = RatoncitoAgent(self.personality)
                self.agent_system = None
                return {
                    "status": "success",
                    "message": "Cambiado a sistema legacy"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error al cambiar sistema: {str(e)}"
            }


# Factory function que mantiene compatibilidad con el código existente
def create_ratoncito_agent(personality: str = None, use_multi_agent: bool = True) -> RatoncitoAgentAdapter:
    """Crea un agente Ratoncito usando el adaptador"""
    return RatoncitoAgentAdapter(personality=personality, use_multi_agent=use_multi_agent)