from collectors import collector
from collectors import docker_health
from models.container_response_model import ContainerPayload
from models.metric_response_model import MetricPayload

from fastapi import APIRouter

METRICS_INTERVAL = 1

router = APIRouter(prefix="/api")


@router.get("/server_metrics", response_model=MetricPayload)
async def get_metrics():
    metric_obj = collector.Metrics(METRICS_INTERVAL)
    all_server_metrics_dict = metric_obj.get_metrics()
    print(all_server_metrics_dict)
    return MetricPayload(**all_server_metrics_dict)


@router.get("/container_status", response_model=ContainerPayload)
async def get_container_info():
    docker_stats_obj = docker_health.Docker_Info()
    all_container_info_dict = docker_stats_obj.get_docker_info()
    return ContainerPayload(**all_container_info_dict)
