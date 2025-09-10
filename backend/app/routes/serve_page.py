import os

from fastapi import APIRouter
from fastapi.responses import HTMLResponse 

# Metrics Page
metric_page_path = os.path.join("web", "metric_page.html")
with open(metric_page_path, "r") as f:
    metric_page = f.read()

# Container Status Page
container_status_path = os.path.join("web", "container_status_page.html")
with open(container_status_path, "r") as f:
    container_status_page = f.read()

page_router = APIRouter()

@page_router.get("/server_metrics")
async def get_server_metrics_page():
    return HTMLResponse(metric_page)

@page_router.get("/container_status")
async def get_container_status_page():
    return HTMLResponse(container_status_page)
