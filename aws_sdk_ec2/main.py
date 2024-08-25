from ec2_lib import action

# EC2のインスタンスのステータスを取得して、ステータスが停止中の場合は起動する
if __name__ == '__main__':

    instance_id = 'i-xxxxxxxxxxxxxxxxx'
    status = action.get_ec2_instance_status(instance_id)

    if status == 'stopped':
        action.start_ec2_instance(instance_id)
        print('EC2を起動中です。しばらくお待ちください。')
    else:
        print('EC2インスタンスは起動中です。')
