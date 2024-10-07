# ECS タスクを正常に終了するためのシグナルハンドラを実装する
import os
import signal
import requests


def _get_task_desired_status():
    try:
        base_url = os.environ["ECS_CONTAINER_METADATA_URI_V4"]
        response = requests.get(f'{base_url}/task')
        metadata = response.json()
        desired_status = metadata['DesiredStatus']
        return desired_status
    except requests.exceptions.RequestException as e:
        print(f"Error fetching instance ID: {e}")
        return None


def task_shutdown(signum, frame):
    exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, task_shutdown)
