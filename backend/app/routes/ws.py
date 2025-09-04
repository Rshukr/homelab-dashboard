from collectors.collector import Metrics

from fastapi import WebSocket, WebSocketException, APIRouter

METRICS_INTERVAL = 1


ws_router = APIRouter(prefix="/ws")

@ws_router.websocket("/server_metrics")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            metric_obj = Metrics(METRICS_INTERVAL)
            metric_data = metric_obj.get_metrics()
            await websocket.send_json(metric_data)
    except:
        return {"msg": "ERROR"}