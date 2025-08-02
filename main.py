from fastapi import FastAPI
from routes import estudo_routes

app = FastAPI(
    title = "API de Gerenciamento de Estudos",
    version = "Beta",
    description= "Estudos"
)
app.include_router(estudo_routes.router)