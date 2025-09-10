##########################################################
#### To launch: uvicorn backend.app.main:app --reload ####
#### To launch on LAN add: --host 0.0.0.0 --port 8000 ####
##########################################################

import os

from routes.api import api_router
from routes.ws import ws_router
from routes.serve_page import page_router

from fastapi import FastAPI
from fastapi.responses import HTMLResponse 

app = FastAPI()
app.include_router(router=api_router)
app.include_router(router=ws_router)
app.include_router(router=page_router)

home_page_path = os.path.join("web", "home.html")
with open(home_page_path, "r") as f:
    home_page = f.read()

@app.get("/")
async def root():
    return HTMLResponse(home_page)
