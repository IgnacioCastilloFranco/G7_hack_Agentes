import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

# Clase para gestionar la configuración de la aplicación, así podemos cambiar fácilmente según qué modelo o agente que queramos usar, lo cambiaremos en el .env

class Settings:
    # API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # Configuración del modelo LLM 
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "groq")  
    LLM_MODEL: str = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")  
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.8")) 
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "1500"))  
    
    # Configuración del Agente
    AGENT_TYPE: str = os.getenv("AGENT_TYPE", "react")  
    AGENT_VERBOSE: bool = os.getenv("AGENT_VERBOSE", "true").lower() == "true"
    AGENT_MAX_ITERATIONS: int = int(os.getenv("AGENT_MAX_ITERATIONS", "5"))
    AGENT_MAX_EXECUTION_SECONDS: int = int(os.getenv("AGENT_MAX_EXECUTION_SECONDS", "30"))
    
    # Configuración del Ratoncito Pérez
    RATONCITO_PERSONALITY: str = os.getenv("RATONCITO_PERSONALITY", "magical_guide")
    RATONCITO_DEFAULT_LOCATION: str = os.getenv("RATONCITO_DEFAULT_LOCATION", "Madrid Centro")

    # Configuración de la base de conocimiento
    KNOWLEDGE_BASE_URL: str = os.getenv("SUPABASE_URL", os.getenv("KNOWLEDGE_BASE_URL", ""))
    KNOWLEDGE_BASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", os.getenv("KNOWLEDGE_BASE_ANON_KEY", ""))
    KNOWLEDGE_BASE_BUCKET: str = os.getenv("SUPABASE_BUCKET", os.getenv("KNOWLEDGE_BASE_BUCKET", ""))
    

settings = Settings()
