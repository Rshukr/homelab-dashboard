##########################################################
#### To launch: uvicorn backend.app.main:app --reload ####
#### To launch on LAN add: --host 0.0.0.0 --port 8000 ####
##########################################################

from routes.api import router

from fastapi import FastAPI

app = FastAPI()
app.include_router(router=router)


@app.get("/")
async def root():
    return {"Main": "Welcome to my Homelab Dashboard"}
