import redis
from strenum import StrEnum


class JobStatus(StrEnum):
    FAILED = "failed"
    SUCCESS = "success"
    NOT_FOUND = "not found"
    IN_PROGRESS = "in progress"


class RedisOperator:

    def __init__(self, redis_url: str):
        host, port = redis_url.split(':')  # TODO: check if it works
        self.redis_client = redis.Redis(host, port)

    def get_job_status(self, job_name: str) -> JobStatus:
        # TODO: get status using correct operations on redis
        pass
