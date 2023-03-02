import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.responses import RedirectResponse

api=FastAPI()
api.mount("/static", StaticFiles(directory="static"), name="static")

# api.include_router(router=router, prefix="/api", tags=["api"])


@api.get("/")
async def root(request:Request):
    return HTMLResponse(content="<h1>Hello World!</h1>")


@api.get("/api/v1/ping")
async def ping():
    return JSONResponse(content={"message":"pong"})


@api.get("/api/v1/redirect")
async def redirect():
    return RedirectResponse("/api/v1/ping")


@api.get("/api/v1/hello")
async def hello():
    return {"message":"hello"}


@api.get("/api/v1/hello/{name}")
async def hello(name:str):
    return {"message":"hello "+name}


@api.get("/api/v1/hello/{name}/{age}")
async def hello(name:str, age:int):
    return {"message":"hello "+name+" "+str(age)}


@api.get("/api/v1/hello/{name}/{age}/{city}")
async def hello(name:str, age:int, city:str):
    return {"message":"hello "+name+" "+str(age)+" "+city}


@api.get("/api/v1/hello/{name}/{age}/{city}/{country}")
async def hello(name:str, age:int, city:str, country:str):
    return {"message":"hello "+name+" "+str(age)+" "+city+" "+country}







