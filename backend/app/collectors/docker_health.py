import json
import os
from collections import defaultdict

import docker

"""

1. list all container ids
2. container = client.container.get(id*)
3. container.stats() # stream = True -> Generator | False -> Dict
4. container.attr # for Id, Name, State, Image

"""

# TEST
FILENAME = "docker_info.json"
OUTPUT_DIR = os.path.join("backend", "output")
CONTAINER_LIST_NAME = "containers"
ERROR_NAME = "error"


class Docker_Info:
    def __init__(self):  # base_url_input, use_ssh_client_input: bool):
        self.docker_container_json = defaultdict(dict)
        try:
            self.client = docker.from_env(
                # base_url=base_url_input, use_ssh_client=use_ssh_client_input
            )
            self.containers = self.client.containers.list()
            self.docker_container_json.clear()
            self._set_all_docker_info()
            self.docker_container_json = dict(self.docker_container_json)
        except docker.errors.DockerException as e:
            self.docker_container_json[ERROR_NAME] = (
                f"Docker might not be installed on the server. Check out the docker error message: {e}"
            )

    def _populate_docker_json(self, container):
        try:
            self.docker_container_json[CONTAINER_LIST_NAME][container.attrs["Name"]] = {
                "short_id": container.short_id,
                "state": container.attrs["State"]["Status"],
                "image": container.image.tags[0],
            }
        except docker.errors.NotFound as e:
            print(f"Problem accessing container. Error: {e}")

    def _set_all_docker_info(self):
        for container in self.containers:
            self._populate_docker_json(container)

    def get_docker_info(self):
        return self.docker_container_json

    def write_docker_info_json(self, output_file):

        with open(output_file, "w") as f:
            json.dump(self.docker_container_json, f, indent=4)

        print(f"Docker info file found at: {output_file}")


if __name__ == "__main__":
    container_info = Docker_Info()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, FILENAME)
    # container_info.get_docker_info_json(output_file)
    # print(container_info.docker_container_json)
