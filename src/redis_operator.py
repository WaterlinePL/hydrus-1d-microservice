import redis
from strenum import StrEnum


class JobStatus(StrEnum):
    FAILED = "failed"
    SUCCESS = "success"
    NOT_FOUND = "not found"
    IN_PROGRESS = "in progress"


class RedisOperator:

    def __init__(self, redis_url: str):
        host, port = redis_url.split(':')
        self.redis_client = redis.Redis(host, port)

    def put_job_command(self, key: str, cmd: str):
        self.redis_client.lpush(key, cmd)

    def get_job_status(self, job_name: str) -> JobStatus:
        # TODO: get status using correct operations on redis (discover which messages)
        #  it might be sth like this:
        job_status = self.redis_client.lpop(job_name)
        if job_status:
            # TODO: Parse the status
            return JobStatus.SUCCESS
        return JobStatus.NOT_FOUND

    def close(self):
        self.redis_client.close()
