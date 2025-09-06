from collectors import collector
from collectors import docker_health
from models.container_response_model import ContainerPayload
from models.metric_response_model import MetricPayload, ServerMetricsResponse

from fastapi import APIRouter

METRICS_INTERVAL = 1

router = APIRouter(prefix="/api")


@router.get("/server_metrics", response_model=MetricPayload)
async def get_metrics() -> MetricPayload:
    metric_obj = collector.Metrics(METRICS_INTERVAL)
    payload_dict = await metric_obj.get_metrics()

    # Convert nested 'data' dict into the expected Pydantic model
    server_metrics = ServerMetricsResponse(**payload_dict["data"])  # type: ignore[arg-type]
    return MetricPayload(
        type=payload_dict["type"],
        ts=payload_dict["ts"],
        data=server_metrics,
    )


@router.get("/container_status", response_model=ContainerPayload)
async def get_container_info():
    docker_stats_obj = docker_health.Docker_Info()
    all_container_info_dict = docker_stats_obj.get_docker_info()
    return ContainerPayload(**all_container_info_dict)
