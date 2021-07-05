from fastapi import APIRouter


demo = APIRouter(
    prefix="/demo",
    tags= ["router_demo"],
    responses={404:{'msg': 'not found'}},
)


@demo.get("/")
async def hello_world():
    return {"Hello":"Opentrons"}