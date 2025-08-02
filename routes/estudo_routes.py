from fastapi import APIRouter, HTTPException
from typing import List
from models.estudo_model import PlanoEstudoRequest, PlanoEstudoResponse
from service.estudo_service import PlanoEstudoService

router = APIRouter(
    prefix="/estudos",
    tags=["Plano de Estudo"]
)
service = PlanoEstudoService()

@router.post("/", response_model = PlanoEstudoResponse)
async def criar_plano(plano: PlanoEstudoRequest):
    return service.criar_plano(plano)


@router.get("/", response_model=List[PlanoEstudoResponse])
async def listar():
    return service.listar_planos()


@router.get("/{id}", response_model=PlanoEstudoResponse)
async def listar_por_id(id):
    plano = service.listar_plano_por_id(id)
    if not plano:
        return HTTPException(404, detail="Plano de estudo não encontrado!")
    else:
        return plano