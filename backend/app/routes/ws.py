from collectors.collector import Metrics
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

ws_router = APIRouter()
INTERVAL = 1
async def get_metric_task(websocket: WebSocket, timer: int):
    try:
        while True:
            metric_obj = Metrics(1)
            metric_data = await metric_obj.get_metrics()
            try:
                await websocket.send_json(metric_data)
            except (WebSocketDisconnect, RuntimeError):
                return
            await asyncio.sleep(timer)
    except asyncio.CancelledError:
        print("Task has been Cancelled")
        raise
        

@ws_router.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    metric_task = asyncio.create_task(get_metric_task(websocket, INTERVAL))
    try:
        while True:
            try:
                await asyncio.wait_for(websocket.receive(), timeout=0.5)
            except (asyncio.TimeoutError, RuntimeError):
                raise
    except WebSocketDisconnect as e:
        print(f"WEBSOCKET CONNECTION CLOSED, CODE: {e.code}")
    finally:
        metric_task.cancel()
        try:
            await metric_task
        except asyncio.CancelledError:
            pass
        print("CLEAN UP PHASE")
