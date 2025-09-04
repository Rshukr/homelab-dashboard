##########################################################
#### To launch: uvicorn backend.app.main:app --reload ####
#### To launch on LAN add: --host 0.0.0.0 --port 8000 ####
##########################################################

from routes.api import router
from routes.ws import ws_router

from fastapi import FastAPI

app = FastAPI()
app.include_router(router=router)
# app.include_router(router=ws_router)


@app.get("/")
async def root():
    return {"Main": "Welcome to my Homelab Dashboard"}

from collectors.collector import Metrics

from fastapi import WebSocket, WebSocketException, APIRouter

METRICS_INTERVAL = 1


# ws_router = APIRouter(prefix="/ws")

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     print("HELLO")
#     await websocket.accept()
#     # try:
#     #     while True:
#     #         metric_obj = Metrics(METRICS_INTERVAL)
#     #         metric_data = metric_obj.get_metrics()
#     #         await websocket.send_json(metric_data)
#     # except:
#         # return {"msg": "ERROR"}
#     return {"msg": "ERROR"}