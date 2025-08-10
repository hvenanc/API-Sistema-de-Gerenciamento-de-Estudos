from passlib.context import CryptContext
from models.usuario_model import *
from config.firebase_config import db


class UsuarioService:


    def __init__(self):
        self.collection = db.collection("usuarios")
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    
    def criar_usuario(self, usuario: UserRequest):
        doc = self.collection.document()
        usuario = UserModel(
            id = doc.id,
            nome = usuario.nome,
            email = usuario.email,
            password = self.get_password_hash(usuario.password)
        )
        doc.set(usuario.model_dump())
        return usuario
    

    def get_user_by_email(self, email: str):
        docs = self.collection.where("email", "==", email).stream()
        for doc in docs:
            return helper(doc)
        return None
    

