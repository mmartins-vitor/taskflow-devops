# import do framework
from fastapi import FastAPI

# instanciando classe FastAPI
app = FastAPI()


# primeira rota
@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao TaskFlow!"}
