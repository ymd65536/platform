import os
import requests
import boto3

ecs = boto3.client('ecs')


def container_arn_by_ecs():
    try:
        base_url = os.environ["ECS_CONTAINER_METADATA_URI_V4"]
        response = requests.get(f'{base_url}/task')
        metadata = response.json()
        container_arn = metadata['TaskARN']
        return container_arn
    except requests.exceptions.RequestException as e:
        print(f"Error fetching instance ID: {e}")
        return None


def _on_task_protection():
    """
    タスク保護
    :param なし:
    :return: なし
    """

    task_arn = container_arn_by_ecs()
    task_id = f"{task_arn.split('/')[-1]}"
    cluster_name = f"{task_arn.split('/')[-2]}"

    res = ecs.update_task_protection(
        cluster=cluster_name,
        tasks=[
            task_id
        ],
        protectionEnabled=True,
        expiresInMinutes=60
    )
    if res.get('failures'):
        # タスク保護失敗
        return False
    else:
        # タスク保護成功
        return True


def _off_task_protection():
    """
    タスク保護解除
    :param なし:
    :return: なし
    """

    task_arn = container_arn_by_ecs()
    task_id = f"{task_arn.split('/')[-1]}"
    cluster_name = f"{task_arn.split('/')[-2]}"

    res = ecs.update_task_protection(
        cluster=cluster_name,
        tasks=[
            task_id
        ],
        protectionEnabled=False,
    )
    if res.get('failures'):
        return False
    else:
        return True
