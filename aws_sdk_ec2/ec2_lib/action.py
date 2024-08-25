# 特定のEC2を起動する
import boto3


def start_ec2_instance(instance_id):
    # EC2インスタンスを起動
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instance_id)
    response = instance.start()
    return response


# 特定のEC2を停止する
def stop_ec2_instance(instance_id):
    # EC2インスタンスを停止
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instance_id)
    response = instance.stop()
    return response


# 特定のEC2のステータスを取得する
def get_ec2_instance_status(instance_id):
    # EC2インスタンスのステータスを取得
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instance_id)
    response = instance.state['Name']
    return response
