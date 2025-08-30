from typing import List, Dict, Union
import json
import os

import psutil

TO_GB = 1e9
TO_MB = 1e6

FILENAME = "test.json"
OUTPUT_DIR = os.path.join("backend", "output")


class Metrics:
    def __init__(self):
        cpu_info = self._collect_cpu()
        mem_info = self._collect_mem()
        disk_info = self._collect_storage()
        net_info = self._collect_net_rates()
        temp_info = self._collect_temp()

        self.metrics_dict = {
            "cpu_info": cpu_info,
            "mem_info": mem_info,
            "disk_info": disk_info,
            "net_info": net_info,
            "temp_info": temp_info,
        }

    def _collect_cpu(self) -> Dict[str, Union[str, Dict[str, str]]]:
        # cpu usage, cpu usage per core

        cpu_usage_per_core = psutil.cpu_percent(interval=1, percpu=True)
        cpu_usage_avg = sum(cpu_usage_per_core) / len(cpu_usage_per_core)

        return {
            "Global CPU Usage": f"{cpu_usage_avg:.2f}",
            "CPU Usage per Core": {
                str(cpu_count): f"{core_usage:.2f}"
                for cpu_count, core_usage in enumerate(cpu_usage_per_core, start=1)
            },
        }

    def _collect_mem(self) -> Dict[str, str]:
        # total, available, usage percent

        all_mem_info = psutil.virtual_memory()

        mem_total = str(all_mem_info.total // TO_GB)
        mem_available = str(all_mem_info.available // TO_GB)
        mem_usage_percent = str(all_mem_info.percent)

        return {
            "Total Memory": mem_total,
            "Available Memory": mem_available,
            "Memory Usage Percentage": mem_usage_percent,
        }

    def _collect_storage(self) -> Dict[str, str]:
        # total, available, used, percent

        all_disk_info = psutil.disk_usage("/")

        disk_total = str(all_disk_info.total // TO_GB)
        disk_free = str(all_disk_info.free // TO_GB)
        disk_used = str(all_disk_info.used // TO_GB)
        disk_percentage = str(all_disk_info.percent)

        return {
            "Total Disk Space": disk_total,
            "Total Free Space": disk_free,
            "Total Space Used": disk_used,
            "Disk Usage Percent": disk_percentage,
        }

    def _collect_net_rates(self) -> Dict[str, str]:
        # download, upload
        return {"Download Speed": "VERY FAST", "Upload Speed": "VERY FAST"}

    def _collect_temp(self) -> Dict[str, str]:
        # global temp (acpitz)

        temp_info = str(psutil.sensors_temperatures()["acpitz"][0].current)

        return {"Global Temperature": f"{temp_info} C"}

    def get_metrics(self, output_file) -> Dict[str, Union[Dict, str]]:

        with open(output_file, "w") as f:
            json.dump(self.metrics_dict, f, indent=4)


if __name__ == "__main__":
    test_metrics = Metrics()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    test_output_file = os.path.join(OUTPUT_DIR, FILENAME)
    test_metrics.get_metrics(test_output_file)

