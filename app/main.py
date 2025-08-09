from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.routes import router as tasks_router
from app.auth import router as auth_router

# Esta linha é a chave: ela cria a tabela "tasks" (e outras, se houver)
# no banco de dados quando a aplicação é iniciada.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow API")

app.include_router(auth_router)  # /register, /login
app.include_router(tasks_router)  # /tasks


@app.get("/")
def read_root():
    return {"message": "Welcome to TaskFlow API"}


# Aqui você adicionaria suas rotas para criar, ler, atualizar e deletar tarefas.
