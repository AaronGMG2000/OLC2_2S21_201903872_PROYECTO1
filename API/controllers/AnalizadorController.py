from fastapi import APIRouter
from shared.models import RequestModel


router = APIRouter()


@router.post('/Compilar')
async def analysis(req: RequestModel):
    try:
        print(req.Contenido)
        return {"salida": req.Contenido}
    except Exception as e:
        return {"error": str(e)}

