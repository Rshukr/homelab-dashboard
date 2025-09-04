from typing import Dict, Union
import json
import os
import itertools
import time

import psutil

TO_GB = 1e9
TO_MB = 1e6
METRICS_INTERVAL = 1
FILENAME = "test.json"
OUTPUT_DIR = os.path.join("backend", "output")


class Metrics:
    def __init__(self, metrics_interval):
        self.metrics_interval = metrics_interval
        
        cpu_info = self._collect_cpu()
        mem_info = self._collect_mem()
        disk_info = self._collect_storage()
        net_info = self._collect_net_rates()
        temp_info = self._collect_temp()

        self.metrics_data_dict = {
            "cpu_info": cpu_info,
            "mem_info": mem_info,
            "disk_info": disk_info,
            "net_info": net_info,
            "temp_info": temp_info,
        }
        
        self.payload = {
            "type": "metrics",
            "ts": str(int(time.time())),
            "data": self.metrics_data_dict
        }

    def _collect_cpu(self) -> Dict[str, Union[str, Dict[str, str]]]:
        # cpu usage, cpu usage per core

        cpu_usage_per_core = psutil.cpu_percent(interval=self.metrics_interval, percpu=True)
        cpu_usage_avg = sum(cpu_usage_per_core) / len(cpu_usage_per_core)

        return {
            "global_cpu_usage": f"{cpu_usage_avg:.2f}",
            "cpu_usage_per_core": {
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
            "total_memory": mem_total,
            "available_memory": mem_available,
            "memory_usage_percentage": mem_usage_percent,
        }

    def _collect_storage(self) -> Dict[str, str]:
        # total, available, used, percent

        all_disk_info = psutil.disk_usage("/")

        disk_total = str(int(all_disk_info.total // TO_GB))
        disk_free = str(int(all_disk_info.free // TO_GB))
        disk_used = str(int(all_disk_info.used // TO_GB))
        disk_percentage = str(int(all_disk_info.percent))

        return {
            "total_disk_space": f"{disk_total} GB",
            "total_free_space": f"{disk_free} GB",
            "total_space_used": f"{disk_used} GB",
            "disk_usage_percent": f"{disk_percentage} %",
        }

    def _collect_net_rates(self) -> Dict[str, str]:
        # TODO: download, upload
        return {"download_speed": "VERY FAST", "upload_speed": "VERY FAST"}

    def _collect_temp(self) -> Dict[str, str]:
        # global temp (acpitz)
        try:
            all_shwtemp = list(itertools.chain.from_iterable(psutil.sensors_temperatures().values()))
            all_temp = [cur_temp.current for cur_temp in all_shwtemp]
            avg_temp = sum(all_temp)/len(all_temp)
            return {"global_temperature": f"{avg_temp} C"}
        except:
            return {"global_temperature": "No temperature Found"}

    def get_metrics(self) -> Dict[str, Union[Dict, str]]:
        return self.payload

    def write_metrics(self, output_file):

        with open(output_file, "w") as f:
            json.dump(self.payload, f, indent=4)


if __name__ == "__main__":
    test_metrics = Metrics(METRICS_INTERVAL)
    # os.makedirs(OUTPUT_DIR, exist_ok=True)
    # test_output_file = os.path.join(OUTPUT_DIR, FILENAME)
    print(test_metrics.get_metrics())
    # test_metrics.write_metrics(test_output_file)
    # print(f"Test metric json found at: {test_output_file}")
