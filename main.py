from typing import Optional, List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Tarefa(BaseModel):
    name: str
    descricao: str

listona = {
    'pegar_vovó_no_jiujistu' : {
        'descricao' : 'vovó ta la no jiujitsu tem q ir buscar', 
        'concluido' :  False 
    },

    'estudar_desComp' : {
        'descricao' : 'ta mt osso', 
        'concluido' :  False 
    },

    'tomar_café' : {
        'descricao' : 'vamo q vamo', 
        'concluido' :  True 
    }
}

@app.get("/") 
async def read_root(checked: Optional[bool] = None):
    
    if checked is not None:

        if checked:
            ret = {k : v for k, v in listona.items() if v['concluido']}
            return ret
        else:
            ret = {k: v for k, v in listona.items() if not v['concluido']}
            return ret

    else:
        return listona




@app.post("/addItem/")
async def create_item(tarefa: Tarefa):
    listona[tarefa.name.replace(" ", "_")] = { 'descricao' : tarefa.descricao, 'concluido' : False }
    return tarefa

@app.patch("/checkItem/{tarefa_nome}")
async def check_item(tarefa_nome: str):
    listona[tarefa_nome]['concluido'] = not listona[tarefa_nome]['concluido']
    return tarefa_nome + ' Checked'

@app.patch("/alterDescription/")
async def alter_description(tarefa: Tarefa):
    listona[tarefa.name.replace(" ", "_")]['descricao'] = tarefa.descricao
    return 'description updated to: ' + tarefa.descricao

@app.delete("/delTask/{tarefa_nome}")
async def delete_task(tarefa_nome: str):
    listona.pop(tarefa_nome)
    return 'Task ~'+tarefa_nome+'~ Removed'

# ---------  testes  -----------

# @app.get("/files/{file_path:path}")
# async def read_file(file_path: str):
#     return {"file_path": file_path}

# @app.get("/items/{item_id}")
# async def read_querry(item_id: str, q: Optional[str] = None, short: bool = False):
#     tarefa = {"item_id": item_id}
#     if q:
#         tarefa.update({"q": q})
#     if not short:
#         tarefa.update(
#             {"description": "This is an amazing tarefa that has a long description"}
#         )
#     if short:
#         tarefa.update(
#             {"description": "blah"}
#         )
#     return tarefa