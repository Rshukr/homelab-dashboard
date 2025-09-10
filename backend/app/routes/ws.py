from collectors.collector import Metrics
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

ws_router = APIRouter(prefix="")
INTERVAL = 0.5
async def get_metric_task(websocket: WebSocket, timer: float):
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
        

@ws_router.websocket("/server_metrics/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    metric_task = asyncio.create_task(get_metric_task(websocket, INTERVAL))
    try:
        while True:
            try:
                await asyncio.wait_for(websocket.receive(), timeout=0.5)
            except asyncio.TimeoutError as e:
                continue
            except (WebSocketDisconnect, RuntimeError):
                break
    except (WebSocketDisconnect, RuntimeError) as e:
        print(f"WEBSOCKET CONNECTION CLOSED, CODE: {e}")
    finally:
        metric_task.cancel()
        try:
            await metric_task
        except asyncio.CancelledError:
            pass
        print("CLEAN UP PHASE")
