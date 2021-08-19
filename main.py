from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

# from Apps.demo_router import demo
# from Apps.Users_router import user_app
from Apps.Test_room import TR_App
import uvicorn



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.include_router(demo)dasdaadsasd
# app.include_router(user_app)
app.include_router(TR_App)


@app.get("/show")
async def show(request:Request):
    return templates.TemplateResponse('html/Volume_Test_Room.html',{"request":request})


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
