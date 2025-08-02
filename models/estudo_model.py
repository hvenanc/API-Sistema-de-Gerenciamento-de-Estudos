from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class StatusEnum(str, Enum):
    criado = "criado"
    iniciado = "iniciado"
    finalizado = "finalizado"


class PlanoEstudoRequest(BaseModel):
    disciplina: str
    descricao: str
    data_fim: datetime


class PlanoEstudoResponse(BaseModel):
    id: str
    disciplina: str
    descricao: str
    status: StatusEnum = StatusEnum.criado
    data_inicio: datetime
    data_fim: datetime


def helper(doc) -> dict:
    data = doc.to_dict()
    data["id"] = doc.id
    return data