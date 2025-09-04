from fastapi import Body
from pydantic import BaseModel


class CpuMetric(BaseModel):
    global_cpu_usage: str
    cpu_usage_per_core: dict[str, str]


class MemMetric(BaseModel):
    total_memory: str
    available_memory: str
    memory_usage_percentage: str


class DiskMetric(BaseModel):
    total_disk_space: str
    total_free_space: str
    total_space_used: str
    disk_usage_percent: str


class NetMetric(BaseModel):
    download_speed: str
    upload_speed: str


class TempMetric(BaseModel):
    global_temperature: str


class ServerMetricsResponse(BaseModel):
    cpu_info: CpuMetric
    mem_info: MemMetric
    disk_info: DiskMetric
    net_info: NetMetric
    temp_info: TempMetric

class MetricPayload(BaseModel):
    type: str
    ts: str
    data: ServerMetricsResponse