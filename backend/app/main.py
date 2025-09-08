from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routes import recommendations

load_dotenv()

app = FastAPI(
    title="Fastapi",
    description="API de prueba con FastAPI",
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



@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API"}