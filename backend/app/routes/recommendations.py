from fastapi import APIRouter

router = APIRouter()

@router.get("/tour")
async def tour_recommendations():
    return {"message": "Aquí están tus recomendaciones de tours"}