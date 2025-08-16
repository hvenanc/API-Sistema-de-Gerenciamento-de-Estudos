from datetime import datetime, timezone
from models.estudo_model import StatusEnum
from config.firebase_config import db
from repository.estudo_repository import PlanoEstudoRepository
from models.estudo_model import PlanoEstudoResponse, PlanoEstudoRequest, PlanoStatusRequest, helper

class PlanoEstudoService:

    def __init__(self):
        self.collection = db.collection("estudos")
        self.repository = PlanoEstudoRepository()


    def criar(self, plano: PlanoEstudoRequest) -> PlanoEstudoResponse:
        doc = self.repository.collection.document()
        plano_estudo = PlanoEstudoResponse(
            id = doc.id,
            disciplina = plano.disciplina,
            descricao = plano.descricao,
            status = StatusEnum.criado.value,
            data_inicio = datetime.now(),
            data_fim = plano.data_fim
        )
        return self.repository.criar(plano_estudo)
    

    def listar_todos_planos(self):
        return self.repository.listar_todos()
    

    def listar_plano_por_id(self, id):
        return self.repository.listar_por_id(id)
    

    def editar_plano(self, id, dados: PlanoEstudoRequest):
        doc = self.repository.listar_por_id(id)

        if not doc:
            return None
        
        else:
            plano = self.repository.atualizar(id, dados.model_dump(exclude_unset=True))
            return helper(plano)
        
    
    def deletar_plano(self, id) -> bool | None:
        doc = self.repository.listar_por_id(id)

        if not doc:
            return None
        return self.repository.deletar(id)

    
    def alterar_status(self, id, dados: PlanoStatusRequest):
        doc = self.repository.listar_por_id(id)

        if not doc:
            return None
        
        else:
            plano = self.repository.atualizar(id, {"status": dados.status.value})
            return helper(plano)


    def filtrar_plano_por_data(self, data_inicial: datetime, data_fim: datetime):
        #Filtra os planos de estudos baseados na data de inicio.
        data_inicial = data_inicial.replace(tzinfo=timezone.utc)
        data_fim = data_fim.replace(tzinfo=timezone.utc)
        return self.repository.filtrar_por_data(data_inicial, data_fim)
    

    def filtrar_plano_por_disciplina(self, disciplina: str):
        return self.repository.filtrar_por_disciplina(disciplina)
    

    def filtrar_plano_por_status(self, status: str):
        return self.repository.filtrar_por_status(status)

