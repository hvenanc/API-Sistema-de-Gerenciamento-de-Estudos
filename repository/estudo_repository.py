from typing import Optional, List
from datetime import datetime
from config.firebase_config import db
from models.estudo_model import PlanoEstudoResponse, PlanoEstudoRequest, helper

class PlanoEstudoRepository:
    

    def __init__(self):
        self.collection = db.collection("estudos")


    def criar(self, plano: PlanoEstudoRequest) -> PlanoEstudoResponse:
        doc_ref = self.collection.document(plano.id)
        doc_ref.set(plano.model_dump())
        return plano
    

    def listar_todos(self) -> Optional[List[PlanoEstudoResponse]]:
        docs = self.collection.stream()
        return [helper(doc) for doc in docs]
    

    def listar_por_id(self, id: str) -> Optional[PlanoEstudoResponse]:
        doc = self.collection.document(id).get()
        return helper(doc) if doc.exists else None
    

    def atualizar(self, id: str, dados: PlanoEstudoRequest) -> Optional[PlanoEstudoResponse]:
        doc_ref = self.collection.document(id)
        doc_ref.update(dados)
        return doc_ref.get()
    

    def deletar(self, id: str) -> bool:
        doc_ref = self.collection.document(id)
        doc_ref.delete()
        return True
    

    def filtrar_por_disciplina(self, disciplina: str) -> Optional[List[PlanoEstudoResponse]]:
        
        planos = self.collection.where("disciplina", "==", disciplina).stream()
        return [helper(plano) for plano in planos]


    def filtrar_por_status(self, status: str) -> Optional[List[PlanoEstudoResponse]]:
        
        planos = self.collection.where("status", "==", status).stream()
        return [helper(plano) for plano in planos]
    

    def filtrar_por_data(self, data_inicial: datetime,  data_fim: datetime) -> Optional[List[PlanoEstudoResponse]]:
        planos_ref = (
        self.collection
        .where("data_inicio", ">=", data_inicial)
        .where("data_inicio", "<=", data_fim)
        )

        consulta = planos_ref.stream()
        return [helper(doc) for doc in consulta]

