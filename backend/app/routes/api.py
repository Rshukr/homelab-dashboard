from collectors import collector
from collectors import docker_health
from models.container_response_model import ContainerResponse
from models.metric_response_model import ServerMetricsResponse

from fastapi import APIRouter

router = APIRouter(prefix="/api")


@router.get("/server_metrics", response_model=ServerMetricsResponse)
async def get_metrics():
    metric_obj = collector.Metrics()
    all_server_metrics_dict = metric_obj.metrics_dict
    print(all_server_metrics_dict)
    return ServerMetricsResponse(**all_server_metrics_dict)


@router.get("/container_status", response_model=ContainerResponse)
async def get_container_info():
    docker_stats_obj = docker_health.Docker_Info()
    all_container_info_dict = docker_stats_obj.docker_container_json
    return ContainerResponse(**all_container_info_dict)
