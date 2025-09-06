from collectors.collector import Metrics

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

ws_router = APIRouter()

@ws_router.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    Done = False
    while not Done:
        # TODO: Add timer input
        metric_obj = Metrics(1)
        metric_data = await metric_obj.get_metrics()
        await websocket.send_json(metric_data)
        await websocket.close()
        Done = True
    # except WebSocketDisconnect:
