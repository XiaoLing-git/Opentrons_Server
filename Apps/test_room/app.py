from random import random

from fastapi import APIRouter
from fastapi import File,UploadFile
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
async def environment_state(room:int =1 , Fixture:str ="F1", temp:float=None,humidity:float=None):
    THIS_DIR = os.path.dirname(__file__)
    config_file = os.path.join(os.path.join(THIS_DIR, "dependencies"), "configs.json")
    configs = load_config_(config_file)
    configs["flags"]["Room" + str(room)][Fixture][1] = temp
    configs["flags"]["Room" + str(room)][Fixture][2] = humidity
    save_config_(config_file,configs)
    return {"response":"ok"}


@TR_App.post("/file/")
async def create_upload_file(filename:str,filestream: bytes = File(...)):
    file_path = filename.split('\\')
    print(file_path[:-1])
    results_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),"Results")
    for f in file_path[:-1]:
        results_path = os.path.join(results_path,f)
    folder_path = results_path
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    results_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "Results")
    for f in file_path:
        # print(f)
        results_path = os.path.join(results_path,f)
    print(results_path)
    with open(results_path,"a+",newline="") as f:
        writer = csv.writer(f, delimiter=',')
        file = filestream.decode()
        file = file.split('\r\n')
        for l in file:
            l = l.split(',')
            writer.writerow(l)
    return {"filename": "ok"}


@TR_App.post("/uploadfile/")
async def create_upload_file(filename:str, file: UploadFile = File(...)):
    results_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "Results")
    file_path = os.path.join(results_path, filename)
    with open(file_path, "a+", newline="") as f:
        writer = csv.writer(f, delimiter=',')
        file = await file.read()
        file = file.decode()
        file = file.split('\r\n')
        for l in file:
            l = l.split(',')
            writer.writerow(l)
        return {"filename": filename}


@TR_App.post("/files/")
async def create_upload_files(filename:str):
        return {"filename": filename}