from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import date


class StatusEnum(str, Enum):
    criado = "criado"
    iniciado = "iniciado"
    finalizado = "finalizado"


class PlanoEstudo(BaseModel):
    id: Optional[str]
    disciplina: str
    descricao: str
    status: StatusEnum = StatusEnum.criado
    data_inicio: date
    data_fim: date

