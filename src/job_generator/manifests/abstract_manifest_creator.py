import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Tuple, ClassVar

YamlManifest = Dict[str, str]
JobName = str


@dataclass
class AbstractManifestCreator(ABC):
    project_name: str
    docker_image: str
    container_name: str

    @abstractmethod
    def _get_job_prefix(self) -> str:
        ...

    @abstractmethod
    def get_redis_command(self) -> str:
        ...

    @abstractmethod
    def create_manifest(self) -> Tuple[YamlManifest, JobName]:
        ...
