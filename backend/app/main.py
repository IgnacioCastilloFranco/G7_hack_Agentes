from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routes import recommendations, agent_routes, narrative_routes
from backend.app.routes import storytelling_routes

load_dotenv()

app = FastAPI(
    title="Fastapi",
    description="API del Ratoncito Pérez, guardián mágico de Madrid",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas principales
app.include_router(recommendations.router, prefix="/recommend", tags=["Recomendaciones"])
app.include_router(agent_routes.router, prefix="/ratoncito", tags=["Agentes"])
app.include_router(narrative_routes.router, prefix="/narrative", tags=["Narrativas"])
app.include_router(storytelling_routes.router, prefix="/activities", tags=["Actividades"])

@app.get("/")
def read_root():
    return {
        "message": "¡Por mis bigotitos! Bienvenidos a la API del Ratoncito Pérez",
        "endpoints": {
            "react_agent": "/ratoncito/chat/react",
            "simple_agent": "/ratoncito/chat/simple",
            "compare_agents": "/ratoncito/compare",
            "interactive_docs": "/ratoncito/docs"
        }
    }



