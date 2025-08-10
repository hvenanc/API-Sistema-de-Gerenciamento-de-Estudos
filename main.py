from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import estudo_routes, usuario_routes

app = FastAPI(
    title = "API de Gerenciamento de Estudos",
    version = "Beta",
    description= "Estudos"
)
app.include_router(estudo_routes.router)
app.include_router(usuario_routes.router)

# Configuração do CORS para ser público
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)