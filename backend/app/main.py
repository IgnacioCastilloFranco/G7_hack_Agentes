from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routes import recommendations, agent_routes, narrative_routes
from app.routes import storytelling_routes

load_dotenv()

app = FastAPI(
    title="Fastapi",
    description="API del Ratoncito Pérez, guardián mágico de Madrid",
    version="1.1.0"
)

@app.on_event("startup")
async def startup_event():
    print("🚀 La aplicación está arrancando... ¡Despertando al Ratoncito Pérez!")
    # Al llamar a esta función, forzamos la creación del agente global por primera vez.
    agent_routes.get_agent_session("startup_session")
    print("✅ ¡El Ratoncito Pérez está listo para la aventura!")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas principales
app.include_router(agent_routes.router, prefix="/ratoncito", tags=["Agentes"])
app.include_router(narrative_routes.router, prefix="/narrative", tags=["Narrativas"])
app.include_router(storytelling_routes.router, prefix="/activities", tags=["Actividades"])

@app.get("/")
def read_root():
    return {
        "message": "¡Por mis bigotitos! Bienvenidos a la API del Ratoncito Pérez",
        "status": "¡Listo para recibir peticiones mágicas!"
    }



