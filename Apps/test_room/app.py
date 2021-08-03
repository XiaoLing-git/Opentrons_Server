from fastapi import APIRouter
import os



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
