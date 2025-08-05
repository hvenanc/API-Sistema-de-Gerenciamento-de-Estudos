from datetime import datetime
from models.estudo_model import StatusEnum
from config.firebase_config import db
from models.estudo_model import PlanoEstudoResponse, PlanoEstudoRequest, helper

class PlanoEstudoService:

    def __init__(self):
        self.collection = db.collection("estudos")


    def criar_plano(self, plano: PlanoEstudoRequest):
        doc = self.collection.document()
        plano_estudo = PlanoEstudoResponse(
            id = doc.id,
            disciplina = plano.disciplina,
            descricao = plano.descricao,
            status = StatusEnum.criado.value,
            data_inicio = datetime.now(),
            data_fim = plano.data_fim
        )
        doc.set(plano_estudo.model_dump())
        return plano_estudo
    

    def listar_planos(self):
        docs = self.collection.stream()
        return [helper(doc) for doc in docs]
    

    def listar_plano_por_id(self, id):
        doc = self.collection.document(id).get()
        return helper(doc) if doc.exists else None
    

    def editar_plano(self, id, dados: PlanoEstudoRequest):
        doc = self.collection.document(id)

        if not doc.get().exists:
            return None
        
        else:
            doc.update(dados.model_dump(exclude_unset=True))
            plano = doc.get()
            return helper(plano)
        
    

    def deletar_plano(self, id):
        doc = self.collection.document(id).get()
        if doc.exists:
            doc.reference.delete()
            return True
        return None

