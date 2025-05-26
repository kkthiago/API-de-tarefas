from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI(
    title="API de Tarefas",
    description="1.0.0",
    contact={
        "name": "Thiago Alves Soares",
        "email": "thiagobrsoares3011@gmail.com"
    }
)

# Segurança
security = HTTPBasic()
meu_user = "admin"
meu_login = "admin"

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
class Tarefa(BaseModel):
    descricao_tarefa: str
    tarefa_conclusao: bool

meu_dict = {}

# Rotas
@app.get("/tarefas")
def get_tarefas(page:int, limit:int=10, credentials: HTTPBasicCredentials = Depends(autentication)):
    if page <1 or limit<1:
        raise HTTPException(
            status_code=400,
            detail="Page ou limit estão com valores inválidos"
        )
    start = (page - 1)* limit
    end = start + limit
    
    tarefas_ordenadas = sorted(meu_dict.items(), key= lambda x: x[0])
    tarefa_paginados=[
        {"nome_tarefa": nome_tarefa,
         "descricao_tarefa": tarefa["descricao_tarefa"],
         "conclusao_tarefa": tarefa["tarefa_conclusao"]}
        for nome_tarefa, tarefa in tarefas_ordenadas[start:end]
        ]
    
    if not meu_dict:
        return {"message": "Não há tarefas existentes!"}
    
    return{
        "page": page,
        "limit": limit,
        "total": len(meu_dict),
        "tarefas": tarefa_paginados
    }
    
    
    

@app.post("/adiciona")
def post_tarefa(tarefa: Tarefa, credentials: HTTPBasicCredentials = Depends(autentication)):
    nome_tarefa = tarefa.descricao_tarefa
    if nome_tarefa in meu_dict:
        raise HTTPException(status_code=400, detail="Essa tarefa já existe...")
    meu_dict[nome_tarefa] = tarefa.dict()
    return {"message": "A tarefa foi criada com sucesso!"}

@app.put("/atualizar/{nome_tarefa}")
def put_tarefa(nome_tarefa: str, tarefa: Tarefa, credentials: HTTPBasicCredentials = Depends(autentication)):
    if nome_tarefa not in meu_dict:
        raise HTTPException(status_code=404, detail="Essa tarefa não foi encontrada!")
    meu_dict[nome_tarefa] = tarefa.dict()
    return {"message": "A tarefa foi atualizada com sucesso!"}

@app.delete("/deletar/{nome_tarefa}")
def delete_tarefa(nome_tarefa: str, credentials: HTTPBasicCredentials = Depends(autentication)):
    if nome_tarefa not in meu_dict:
        raise HTTPException(status_code=404, detail="Essa tarefa não foi encontrada...")
    del meu_dict[nome_tarefa]
    return {"message": "Sua tarefa foi deletada com sucesso!"}
