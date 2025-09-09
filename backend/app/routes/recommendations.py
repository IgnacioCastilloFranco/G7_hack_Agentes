from fastapi import APIRouter

router = APIRouter()

@router.get("/recommend")
async def recommend():
    return {"message": "Hola, soy el Ratoncito Pérez"}

@router.get("/tour")
async def tour_recommendations():
    return {"message": "Aquí están tus recomendaciones de tours"}