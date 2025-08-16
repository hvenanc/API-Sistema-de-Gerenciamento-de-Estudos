from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import datetime
from models.estudo_model import PlanoEstudoRequest, PlanoEstudoResponse, PlanoStatusRequest
from service.estudo_service import PlanoEstudoService

router = APIRouter(
    prefix="/estudos",
    tags=["Plano de Estudo"]
)
service = PlanoEstudoService()

@router.post("/", response_model = PlanoEstudoResponse, status_code=201)
async def criar_plano(dados: PlanoEstudoRequest):
    return service.criar(dados)


@router.get("/", response_model=List[PlanoEstudoResponse])
async def listar_todos_planos():
    return service.listar_todos_planos()


@router.get("/periodo", response_model=List[PlanoEstudoResponse])
async def buscar_plano_por_periodo(
    data_inicial: datetime = Query(description="Data Inicial"),
    data_fim: datetime = Query(description="Data Final")
):
    planos = service.filtrar_plano_por_data(data_inicial, data_fim)

    if not planos:
        raise HTTPException(404, detail="Nenhum plano de estudo encontrado!")
    return planos


@router.get("/disciplina", response_model=List[PlanoEstudoResponse])
async def buscar_plano_por_disciplina(
    disciplina: str = Query(description="Disciplina")
):
    planos = service.filtrar_plano_por_disciplina(disciplina)
    if not planos:
        raise HTTPException(404, detail="Nenhum plano de estudo encontrado para disciplina!")
    return planos


@router.get("/status", response_model=List[PlanoEstudoResponse])
async def buscar_plano_por_status(
    status: str = Query(description="Status")
):
    planos = service.filtrar_plano_por_status(status)
    if not planos:
        raise HTTPException(404, detail="Nenhum plano de estudo encontrado para o status!")
    return planos


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
    

@router.patch("/{id}", response_model=PlanoEstudoResponse)
async def atualizar_status_plano(id: str, status: PlanoStatusRequest):
    plano = service.listar_plano_por_id(id)
    if plano:
        return service.alterar_status(id, status)
    else:
        raise HTTPException(404, detail="Plano de estudo não encontrado!")
    

