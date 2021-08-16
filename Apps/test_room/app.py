from fastapi import APIRouter
from fastapi import File
from starlette.responses import FileResponse


import os
import csv



from .dependencies.config import load_config_,save_config_



TR_App = APIRouter(tags=["API for Volume QC Room"],
                   prefix="/VQ1")

def init():
    THIS_DIR = os.path.dirname(__file__)
    config_file = os.path.join(os.path.join(THIS_DIR,"dependencies"),"configs.json")
    configs = load_config_(config_file)
    return configs


@TR_App.get("/")
async def hello_test_room():
    return {"hello":"Volume_qc room"}


@TR_App.get("/room")
async def Fixture_list(room_id:int=1):
    THIS_DIR = os.path.dirname(__file__)
    config_file = os.path.join(os.path.join(THIS_DIR, "dependencies"), "configs.json")
    configs = load_config_(config_file)
    res = configs["config"]["Room" + str(room_id)]
    return res


@TR_App.get("/fixture_state")
async def Fixture_state(room_id:int=1):
    THIS_DIR = os.path.dirname(__file__)
    config_file = os.path.join(os.path.join(THIS_DIR, "dependencies"), "configs.json")
    configs = load_config_(config_file)
    res = configs["flags"]["Room" + str(room_id)]
    return res


@TR_App.get("/environment")
async def environment_state(room:int =1 , Fixture:str ="F1", status:str=None ,temp:float=None,humidity:float=None):
    THIS_DIR = os.path.dirname(__file__)
    config_file = os.path.join(os.path.join(THIS_DIR, "dependencies"), "configs.json")
    configs = load_config_(config_file)
    configs["flags"]["Room" + str(room)][Fixture][0] = status
    configs["flags"]["Room" + str(room)][Fixture][1] = temp
    configs["flags"]["Room" + str(room)][Fixture][2] = humidity
    save_config_(config_file,configs)
    return {"response":"ok"}


@TR_App.post("/file/")
async def create_upload_file(filename:str,filestream: bytes = File(...)):
    file_path = filename.split('\\')
    # print(file_path[:-1])
    results_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),"Results")
    for f in file_path[:-1]:
        results_path = os.path.join(results_path,f)
    folder_path = results_path
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    results_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "Results")
    for f in file_path:
        results_path = os.path.join(results_path,f)
    with open(results_path,'w', newline='') as f:
        writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        file = filestream.decode()
        file = file.replace('\n','@').replace('\r\n','@').replace('\n\r','@').replace('\r','@').replace('@@','@')
        # print(file)
        file = file.split('@')
        # print(file)
        for l in file:
            res = l.split(',')
            # print(res)
            writer.writerow(res)
    return {"filename": "ok"}


@TR_App.get("/date_list/")
async def date_list():
    THIS_DIR = os.path.dirname(__file__)
    Results = os.path.join(THIS_DIR, "Results")
    Results_list = os.listdir(Results)
    Results_list.reverse()
    return {"date_list":Results_list}


@TR_App.get("/files_list/")
async def files_list(date:str):
    THIS_DIR = os.path.dirname(__file__)
    Results = os.path.join(os.path.join(THIS_DIR, "Results"), date)
    Results_list = os.listdir(Results)
    return {"files_list":Results_list}


@TR_App.get("/pipette_list/")
async def pipette_list(date:str,model:str):
    # Model must be [P20S,P3HS,P1KS,P20M,P3HM]
    THIS_DIR = os.path.dirname(__file__)
    Results = os.path.join(os.path.join(THIS_DIR, "Results"), date)
    Results_list = os.listdir(Results)
    pipettes_list= []
    for i in Results_list:
        if model in i and i.endswith(".csv"):
            pipettes_list.append(i)
    return {"pipettes_list":pipettes_list}


@TR_App.get("/download/")
def download(date:str,file_name: str):
    THIS_DIR = os.path.dirname(__file__)
    Results = os.path.join(os.path.join(THIS_DIR, "Results"), date)
    file_path = os.path.join(Results, file_name)
    return FileResponse(path=file_path,filename=file_name)



