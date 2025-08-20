from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.routes import router as tasks_router
from app.auth import router as auth_router

app = FastAPI(title="TaskFlow API")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(tasks_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to TaskFlow API"}
