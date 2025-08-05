from datetime import datetime, timezone
from models.estudo_model import StatusEnum
from config.firebase_config import db
from models.estudo_model import PlanoEstudoResponse, PlanoEstudoRequest, PlanoStatusRequest, helper

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

    
    def alterar_status(self, id, dados: PlanoStatusRequest):
        doc = self.collection.document(id)
        plano = doc.get()
        if not plano.exists:
            return None
        
        doc.update({"status": dados.status.value})
        return helper(doc.get())


    def filtrar_plano_por_data(self, data_inicial: datetime, data_fim: datetime):
        #Filtra os planos de estudos baseados na data de inicio.
        data_inicial = data_inicial.replace(tzinfo=timezone.utc)
        data_fim = data_fim.replace(tzinfo=timezone.utc)

        planos_ref = self.collection.where("data_inicio", "<=", data_fim)
        consulta = planos_ref.stream()
        planos_no_intervalo = []
        for doc in consulta:
            plano = helper(doc)

            if plano.get("data_fim") and plano["data_fim"] >= data_inicial:
                planos_no_intervalo.append(plano)
        
        return planos_no_intervalo
    

    def filtrar_plano_por_disciplina(self, disciplina: str):

        planos = self.collection.where("disciplina", "==", disciplina).stream()
        return [helper(plano) for plano in planos]
    

    def filtrar_plano_por_status(self, status: str):

        planos = self.collection.where("status", "==", status).stream()
        return [helper(plano) for plano in planos]

