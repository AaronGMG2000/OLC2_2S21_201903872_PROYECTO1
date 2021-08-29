from fastapi import APIRouter
from shared.models import RequestModel
from ANALIZADOR import grammar as gramatica
from ANALIZADOR.GENERAL.Arbol import Arbol


router = APIRouter()


@router.post('/Compilar')
async def analysis(req: RequestModel):
    try:
        h = gramatica.parse(req.Contenido)
        ast = Arbol(h)
        ast.ejecutar()
        gramatica.start = ""
        return {"consola": ast.getConsola(), "Simbolo": ast.Lista_Simbolo.getLista(), "Errores": ast.errores}
    except Exception as e:
        return {"error": str(e)}
