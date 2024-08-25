# EC2のオートスケーリンググループの設定を変更する

import boto3
import os


# インスタンス数を変更する
def change_capacity(asg_name, min_capacity, max_capacity, desired_capacity, region_name=os.environ["REGION_NAME"]):
    client = boto3.client("autoscaling", region_name=region_name)
    response = client.update_auto_scaling_group(
        AutoScalingGroupName=asg_name,
        MinSize=min_capacity,
        MaxSize=max_capacity,
        DesiredCapacity=desired_capacity,
    )
    print(response)


# オートスケーリンググループの設定を取得する
def get_asg(asg_name, region_name=os.environ["REGION_NAME"]):
    client = boto3.client("autoscaling", region_name=region_name)
    response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
    if response["AutoScalingGroups"]:
        capacities = {
            "MinSize": response["AutoScalingGroups"][0]["MinSize"],
            "MaxSize": response["AutoScalingGroups"][0]["MaxSize"],
            "DesiredCapacity": response["AutoScalingGroups"][0]["DesiredCapacity"],
        }
        return capacities
    else:
        capacities = {}
        return capacities


# メイン関数
def main():
    ec2_capacities = get_asg(os.environ["ASG_NAME"])
    print(ec2_capacities)
    change_capacity(os.environ["ASG_NAME"], 0, 0, 0)
    ec2_capacities = get_asg(os.environ["ASG_NAME"])
    print(ec2_capacities)


if __name__ == "__main__":
    main()
