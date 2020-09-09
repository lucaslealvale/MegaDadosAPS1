from typing import Optional, List
from fastapi import FastAPI
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
    uuid.uuid4().int : {
        'nome'       : 'pegar vovó no jiujistu',
        'descricao'  : 'vovó ta la no jiujitsu tem q ir buscar', 
        'concluido'  :  False 
    },

    uuid.uuid4().int : {
        'nome'       : 'estudar desComp',
        'descricao'  : 'ta mt osso', 
        'concluido'  :  False 
    },

    uuid.uuid4().int : {
        'nome'       : 'tomar café',
        'descricao'  : 'vamo q vamo', 
        'concluido'  :  True 
    }
}

@app.get("/", tags=["Get tasks"]) 
async def read_root(checked: Optional[bool] = None):
    if checked is not None:
        if checked:
            return {k:v for k,v in listona.items() if v['concluido']}
        else:
            return {k:v for k,v in listona.items() if not v['concluido']}
    else:
        return listona
    
@app.get("/{uuid}", tags=["Get tasks"])
async def read_task(uuid: int):
    return {k:v for k,v in listona.items() if k == uuid}

@app.post("/addItem/", tags=["Add tasks"])
async def create_item(tarefa: Tarefa):
    listona[uuid.uuid4().int] = { 'nome' : tarefa.name, 'descricao' : tarefa.descricao, 'concluido' : False }
    return tarefa

@app.patch("/checkItem/{uuid}", tags=["Edit tasks"])
async def check_item(uuid: int):
    listona[uuid]['concluido'] = not listona[uuid]['concluido']
    return listona[uuid]['nome'] + ' Checked'

@app.patch("/alterDescription/{uuid}", tags=["Edit tasks"])
async def alter_description(uuid: int, tarefa: TarefaDescricao):
    listona[uuid]['descricao'] = tarefa.descricao
    return 'description updated to: ' + tarefa.descricao

@app.delete("/delTask/{uuid}", tags=["Remove tasks"])
async def delete_task(uuid: int):
    listona.pop(uuid)
    return 'Task removed'