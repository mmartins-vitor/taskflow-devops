# app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool  # <<

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://taskflow:secret@db:5432/taskflowdb"
)

engine_kwargs = {}
connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    # Para SQLite (e especialmente :memory:), use StaticPool e desabilite check_same_thread
    connect_args = {"check_same_thread": False}
    # Se for memória, precisamos de StaticPool para compartilhar a MESMA conexão
    if ":memory:" in DATABASE_URL:
        engine_kwargs["poolclass"] = StaticPool

engine = create_engine(DATABASE_URL, connect_args=connect_args, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
