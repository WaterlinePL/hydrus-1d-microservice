import redis
from strenum import StrEnum


class JobStatus(StrEnum):
    FAILED = "failed"
    SUCCESS = "success"
    PENDING = "pending"
    RUNNING = "running"
    NOT_FOUND = "not found"


class RedisOperator:

    def __init__(self, redis_url: str):
        host, port = redis_url.split(':')
        self.redis_client = redis.Redis(host, port)

    def put_job_command(self, key: str, cmd: str):
        self.redis_client.lpush(key, cmd)

    def get_job_status(self, job_name: str) -> JobStatus:
        job_key_prefix = f"wf:{job_name}"
        was_initialized = self.redis_client.llen(f"{job_key_prefix}_msg") > 0

        if was_initialized:
            job_exec_statuses = set(int(status) for status in self.redis_client.smembers(job_key_prefix))
            acq_count = self.redis_client.get(f"{job_key_prefix}_acqCount")
            was_acquired = acq_count is not None and int(acq_count) > 0
            completed_successfully = 0 in job_exec_statuses
            is_failed = all(status != 0 for status in job_exec_statuses)

            # Order is very important
            if completed_successfully:
                return JobStatus.SUCCESS
            elif not was_acquired:
                return JobStatus.PENDING
            elif is_failed:
                return JobStatus.FAILED
            elif was_acquired:
                return JobStatus.RUNNING
        return JobStatus.NOT_FOUND

    def close(self):
        self.redis_client.close()
