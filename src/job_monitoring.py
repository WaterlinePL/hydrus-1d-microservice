def watch(
        self,
        tail_logs=False,
        tail_logs_every=None,
        tail_logs_line_count=100,
        sleep_time=5,
        running_timeout=None,
):
    job = self.get()
    total_time = 0
    log_cycles = 1
    while True:
        if not job:
            return False

        completed = bool(job.status.succeeded)
        if completed:
            if bool(tail_logs_every) or tail_logs:
                logging.info(f'Final log output for Job "{self.kube_yaml.name}"')
                self._tail_pod_logs(tail_logs_line_count)
            logging.info(f'Job "{self.kube_yaml.name}" status is Completed')
            return True
        if running_timeout and total_time > running_timeout:
            pass  # running timeout exceeded, probably just a warning, would allow task to continue

        failed = bool(job.status.failed)
        if failed:
            if bool(tail_logs_every) or tail_logs:
                self._tail_pod_logs(tail_logs_line_count)
            raise KubernetesJobLauncherPodError(
                f'Job "{self.kube_yaml.name}" in Namespace "{self.kube_yaml.namespace}" ended in Error state'
            )
        if bool(tail_logs_every):
            if total_time > 0 and total_time % (tail_logs_every // sleep_time) == 0:
                logging.info(f"Beginning new log dump cycle :: {log_cycles}")
                had_logs = self._tail_pod_logs(tail_logs_line_count)
                no_logs_msg = (
                    ", no logs found to output this cycle" if not had_logs else ""
                )
                logging.info(f"Log dump cycle {log_cycles} complete{no_logs_msg}")
                log_cycles += 1

        time.sleep(sleep_time)
        total_time += sleep_time
        job = self.get()
