import requests


class ClientRequestException(Exception):
    pass


class TrainingMasterClient:
    def __init__(self):
        import os
        self.__report_percentage = -1
        self._master_address = os.environ.get("TRAINING_MASTER_ADDRESS")
        self._master_api_version = os.environ.get("TRAINING_MASTER_API_VERSION")
        self._job_metadata = {
            "job_id": os.environ.get("TRAINING_MASTER_JOB_ID"),
            "notice_interval": os.environ.get("TRAINING_MASTER_NOTICE_INTERVAL", 1)
        }
        print(f"[INFO] init training master client {self._master_address}/{self._master_api_version}")

    @property
    def job_metadata(self):
        return self._job_metadata

    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        url = f"http://{self._master_address}/{self._master_api_version}/{endpoint}"
        response = requests.request(method=method, url=url, **kwargs)
        if response.status_code == 200 or response.status_code == 206:
            res = response.json()
            return res
        raise ClientRequestException(f"request training master api error: {response.text}")

    def progress_report(self, cur_progress: int, total_progress: int):
        notice_interval = self._job_metadata["notice_interval"]
        percentage = 100 if total_progress < 1 else int(cur_progress * 100 / total_progress)
        if (percentage % notice_interval != 0 or self.__report_percentage == percentage) and percentage != 100:
            return

        self.__report_percentage = percentage
        job_id = self._job_metadata["job_id"]
        try:
            return self._request("PUT", "job/step", json={
                "job_id": job_id,
                "current_step": percentage,
                "total_step": total_progress
            }).get("data")
        except Exception as e:
            print(f"[WARN] report progress {percentage}%/{total_progress} error: {e.__str__()}")
            return {}

