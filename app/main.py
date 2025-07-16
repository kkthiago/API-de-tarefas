from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import os

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tarefas.db")


app = FastAPI(
    title="API de Tarefas",
    description="1.0.0",
    contact={
        "name": "Thiago Alves Soares",
        "email": "thiagobrsoares3011@gmail.com"
    }
)


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

meu_user = os.getenv("meu_user")
meu_login = os.getenv("meu_login")

# Segurança
security = HTTPBasic()

def autentication(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, meu_user)
    is_password_correct = secrets.compare_digest(credentials.password, meu_login)
    
    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha incorretos.",
            headers={"WWW-Authenticate": "Basic"}
        )

# Modelo e armazenamento
class TarefaDB(Base):
    __tablename__ = "Tarefas"
    id_tarefa = Column(Integer, primary_key=True, index=True)
    nome_tarefa = Column(String, index=True)
    descricao_tarefa = Column(String, index=True)
    conclusao_tarefa = Column(Boolean, index=True)
    
class Tarefa(BaseModel):
    id_tarefa: int
    nome_tarefa: str
    descricao_tarefa: str
    concluso_tarefa: bool
    
Base.metadata.create_all(bind=engine)

meu_dict = {}

def sessao_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Rotas
@app.get("/tarefas")
def get_tarefas(page:int, limit:int=10, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autentication)):
    if page <1 or limit<1:
        raise HTTPException(
            status_code=400,
            detail="Page ou limit estão com valores inválidos"
        )
        
    tarefa = db.query(TarefaDB).offset((page - 1)* limit).limit(limit).all()
    
    if not tarefa:
        return {"message": "Não há tarefas existentes!"}
    
    total_tarefas = db.query(TarefaDB).count()
    
    return{
        "page": page,
        "limit": limit,
        "total": total_tarefas,
        "tarefas": [{"id_tarefa": tarefas.id_tarefa, "nome_tarefa": tarefas.nome_tarefa,"descricao_tarefa": tarefas.descricao_tarefa,"conclusao_tarefa": tarefas.tarefa_conclusao}
        for tarefas in tarefa]
    }

@app.post("/adiciona")
def post_tarefa(tarefa: Tarefa, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autentication)):
    db_tarefa = db.query(TarefaDB).filter(TarefaDB.id_tarefa == tarefa.id_tarefa, TarefaDB.nome_tarefa == tarefa.nome_tarefa).first()
    if db_tarefa:
        raise HTTPException(status_code=400, detail="Esse livro já existe dentro do banco de dados.")
    
    nova_tarefa = TarefaDB(id_tarefa=tarefa.id_tarefa, nome_tarefa=tarefa.nome_tarefa, descricao_tarefa=tarefa.descricao_tarefa, conclusao_tarefa=tarefa.concluso_tarefa)
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    
    return{"message": "A tarefa foi criada com sucesso!"}

@app.put("/atualizar/{id_tarefa}")
def put_tarefa(id_tarefa: int, tarefa: Tarefa, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autentication)):
    db_tarefa = db.query(TarefaDB).filter(TarefaDB.id_tarefa == id_tarefa).first()
    if not db_tarefa:
        raise HTTPException(status_code=404, detail="Esse livro não foi encontrado no seu banco de dados!")
    
    db_tarefa.nome_tarefa = tarefa.nome_tarefa
    db_tarefa.descricao_tarefa = tarefa.descricao_tarefa
    db_tarefa.conclusao_tarefa = tarefa.concluso_tarefa
    db.commit()
    db.refresh(db_tarefa)
    
    return{"message": "O livro foi atualizado com sucesso!"}
    
@app.delete("/deletar/{id_tarefa}")
def delete_tarefa(id_tarefa : int, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autentication)):
    db_tarefa = db.query(TarefaDB).filter(TarefaDB.id_tarefa == id_tarefa).first()
    
    if not db_tarefa:
        raise HTTPException(status_code=404, detail="Esse livro não foi encontrado no seu banco de dados!")
    
    db.delete(db_tarefa)
    db.commit()
    
    return{"message": "O livro foi apagado com sucesso!"}