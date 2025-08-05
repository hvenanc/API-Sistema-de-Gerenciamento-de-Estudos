from fastapi import APIRouter, HTTPException
from typing import List
from models.estudo_model import PlanoEstudoRequest, PlanoEstudoResponse
from service.estudo_service import PlanoEstudoService

router = APIRouter(
    prefix="/estudos",
    tags=["Plano de Estudo"]
)
service = PlanoEstudoService()

@router.post("/", response_model = PlanoEstudoResponse, status_code=201)
async def criar_plano(dados: PlanoEstudoRequest):
    return service.criar_plano(dados)


@router.get("/", response_model=List[PlanoEstudoResponse])
async def listar():
    return service.listar_planos()


@router.get("/{id}", response_model=PlanoEstudoResponse)
async def listar_por_id(id: str):
    plano = service.listar_plano_por_id(id)
    if plano:
        return plano
    else:
        raise HTTPException(404, detail="Plano de estudo não encontrado!")
    

@router.put("/{id}", response_model=PlanoEstudoResponse, status_code=200)
async def atualizar_plano(id: str, dados: PlanoEstudoRequest):
    plano = service.listar_plano_por_id(id)
    if plano:
        return service.editar_plano(id, dados)
    else:
        raise HTTPException(status_code=404, detail="Plano de estudo não encontrado!")
    

@router.delete("/{id}", status_code=204)
async def deletar_por_id(id: str):
    plano = service.listar_plano_por_id(id)
    if plano:
        service.deletar_plano(id)
    else:
        raise HTTPException(404, detail="Plano de estudo não encontrado!")