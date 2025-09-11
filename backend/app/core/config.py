import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

# Clase para gestionar la configuración de la aplicación, así podemos cambiar fácilmente según qué modelo o agente que queramos usar, lo cambiaremos en el .env

class Settings:
    # API Keys
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    # GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY", "")
    
    # Configuración del modelo LLM 
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "groq")  
    LLM_MODEL: str = os.getenv("LLM_MODEL", "Llama-3.3-70B-Versatile")  
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.2")) 
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "1500"))  
    
    # Configuración del Agente
    AGENT_TYPE: str = os.getenv("AGENT_TYPE", "react")  
    AGENT_VERBOSE: bool = os.getenv("AGENT_VERBOSE", "true").lower() == "true"
    AGENT_MAX_ITERATIONS: int = int(os.getenv("AGENT_MAX_ITERATIONS", "4"))
    
    # Configuración del Ratoncito Pérez
    RATONCITO_PERSONALITY: str = os.getenv("RATONCITO_PERSONALITY", "magical_guide")
    RATONCITO_DEFAULT_LOCATION: str = os.getenv("RATONCITO_DEFAULT_LOCATION", "Madrid Centro")

settings = Settings()
