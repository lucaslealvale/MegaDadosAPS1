from fastapi import FastAPI, HTTPException

from typing import Optional, List
from pydantic import BaseModel

import uuid


tags_metadata = [
    {
        "name": "Get tasks",
        "description": "Listar tarefas"
    },
    {
        "name": "Add tasks",
        "description": "Adicionar tarefa"
    },
    {
        "name": "Edit tasks",
        "description": "Editar tarefa"
    },
    {
        "name": "Remove tasks",
        "description": "Remover tarefa"
    }
]

app = FastAPI(
    title="Megadados APS-1",
    description="Feito por Pedro e Lucas",
    openapi_tags=tags_metadata
)

class Tarefa(BaseModel):
    name: str
    descricao: str

class TarefaDescricao(BaseModel):
    descricao: str

listona = {
    uuid.uuid4() : {
        'nome'       : 'pegar vovó no jiujistu',
        'descricao'  : 'vovó ta la no jiujitsu tem q ir buscar', 
        'concluido'  :  False 
    },

    uuid.uuid4() : {
        'nome'       : 'estudar desComp',
        'descricao'  : 'ta mt osso', 
        'concluido'  :  False 
    },

    uuid.uuid4() : {
        'nome'       : 'tomar café',
        'descricao'  : 'vamo q vamo', 
        'concluido'  :  True 
    }
}

@app.get("/", tags=["Get tasks"]) 
async def lista_tasks(checked: Optional[bool] = None):
    """
    **Selecione tarefas:**
    
    - **--**   : Busca todas as tarefas disponiveis
    
    - **true** : Busca as tarefas concluidas

    - **false**: Busca as tarefas incompletas
    """
    if checked is not None:
        if checked:
            return {k:v for k,v in listona.items() if v['concluido']}
        else:
            return {k:v for k,v in listona.items() if not v['concluido']}
    else:
        return listona
    
    
@app.get("/{uuid}", tags=["Get tasks"])
async def lista_task(uuid: uuid.UUID):
    """
    Listar uma task específica do banco de dados:

    - **uuid**: identificador único da tarefa alvo
    """
    if uuid not in listona:
        raise HTTPException(status_code=404, detail="Item not found")

    return {k:v for k,v in listona.items() if k == uuid}


@app.post("/addItem/", tags=["Add tasks"], status_code=201)
async def adiciona_task(tarefa: Tarefa):
    """
    Adiciona uma tarefa ao banco de dados:

    - **nome**: A tarefa precisa ter um nome
    - **descricao**: A tarefa precisa ter uma descrição
    """
    thisUuid = uuid.uuid4()
    listona[thisUuid] = { 'nome' : tarefa.name, 'descricao' : tarefa.descricao, 'concluido' : False }
    return {thisUuid : listona[thisUuid]}

@app.patch("/checkItem/{uuid}", tags=["Edit tasks"])
async def check_task(uuid: uuid.UUID):
    """
    Altere o status de uma terefa:

    - **uuid**: Este parâmetro indica qual tarefa deve ter seu status alternado. 
    """
    if uuid not in listona:
        raise HTTPException(status_code=404, detail="Item not found")

    listona[uuid]['concluido'] = not listona[uuid]['concluido']
    return {uuid : listona[uuid]}

@app.patch("/alterDescription/{uuid}", tags=["Edit tasks"])
async def alterar_descricao(uuid: uuid.UUID, tarefa: TarefaDescricao):
    """
    Alterar a descrição de uma tarefa:

    - **uuid**: Parâmetro fornecido para identificar a tarefa alvo
    - **descricao**: Nova descrição da tarefa
    """

    if uuid not in listona:
        raise HTTPException(status_code=404, detail="Item not found")

    listona[uuid]['descricao'] = tarefa.descricao
    return {uuid : listona[uuid]}

@app.delete("/delTask/{uuid}", tags=["Remove tasks"])
async def deletar_task(uuid: uuid.UUID):
    """
    Remover uma tarefa:

    - **uuid**: Parâmetro fornecido para identificar a tarefa alvo
    """

    if uuid not in listona:
        raise HTTPException(status_code=404, detail="Item not found")

    listona.pop(uuid)
    return f'Task {uuid} removed'