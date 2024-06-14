# Mountpoint for S3を使ってEC2にS3バケットをマウントする

## はじめに

この記事ではMountpoint for S3を使って、EC2にS3バケットをマウントする触る話を書きます。主な内容としては実践したときのメモを中心に書きます。（忘れやすいことなど）
誤りなどがあれば修正していく想定です。

## Mountpoint for S3とは

Mountpoint for S3は、S3バケットをディスクストレージにマウントするためのツールです。

- [Mountpoint for S3](https://aws.amazon.com/jp/blogs/news/mountpoint-for-amazon-s3-generally-available-and-ready-for-production-workloads/)

なるほど？って感じですよね？「百聞は一ハンズオンにしかず」ということで実際に触ってみましょう。

## 検証環境を作成

今回は、EC2インスタンスを使って検証環境を作成します。操作を簡略化するためにCloudFormationを使って検証環境を作成します。テンプレートは以下の通りです。

```yaml:ec2.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: CloudFormation template to create a VPC, and an EC2 instance within that VPC with a specified IAM role for Systems Manager

Parameters:
  EC2ImageId:
    Type: AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>
    Default: "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-6.1-x86_64"

Resources:
  VPC:
    Type: 'AWS::EC2::VPC'
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsSupport: true
      EnableDnsHostnames: true
      Tags:
        - Key: Name
          Value: MyVPC

  InternetGateway:
    Type: 'AWS::EC2::InternetGateway'
    Properties: 
      Tags:
        - Key: Name
          Value: MyInternetGateway

  AttachGateway:
    Type: 'AWS::EC2::VPCGatewayAttachment'
    Properties: 
      VpcId: !Ref VPC
      InternetGatewayId: !Ref InternetGateway

  PublicSubnet:
    Type: 'AWS::EC2::Subnet'
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.1.0/24
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: MyPublicSubnet

  RouteTable:
    Type: 'AWS::EC2::RouteTable'
    Properties:
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: MyRouteTable

  PublicRoute:
    Type: 'AWS::EC2::Route'
    DependsOn: AttachGateway
    Properties:
      RouteTableId: !Ref RouteTable
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref InternetGateway

  SubnetRouteTableAssociation:
    Type: 'AWS::EC2::SubnetRouteTableAssociation'
    Properties:
      SubnetId: !Ref PublicSubnet
      RouteTableId: !Ref RouteTable

  InstanceSecurityGroupA:
    Type: 'AWS::EC2::SecurityGroup'
    Properties:
      VpcId: !Ref VPC
      GroupDescription: Allow HTTPS traffic for SSM
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: '443'
          ToPort: '443'
          CidrIp: 0.0.0.0/0

  InstanceSecurityGroupB:
    Type: 'AWS::EC2::SecurityGroup'
    Properties:
      VpcId: !Ref VPC
      GroupDescription: Allow HTTPS traffic for SSM
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: '443'
          ToPort: '443'
          CidrIp: 0.0.0.0/0

  MyInstanceA:
    Type: 'AWS::EC2::Instance'
    Properties: 
      InstanceType: t3.micro
      ImageId: !Ref EC2ImageId
      IamInstanceProfile: !Ref SSMRoleInstanceProfile
      SecurityGroupIds: 
        - !Ref InstanceSecurityGroupA
      SubnetId: !Ref PublicSubnet
      Tags:
        - Key: Name
          Value: MyEC2InstanceA

  MyInstanceB:
    Type: 'AWS::EC2::Instance'
    Properties: 
      InstanceType: t3.micro
      ImageId: !Ref EC2ImageId
      IamInstanceProfile: !Ref SSMRoleInstanceProfile
      SecurityGroupIds: 
        - !Ref InstanceSecurityGroupB
      SubnetId: !Ref PublicSubnet
      Tags:
        - Key: Name
          Value: MyEC2InstanceB


  SSMRoleInstanceProfile:
    Type: 'AWS::IAM::InstanceProfile'
    Properties: 
      Roles: 
        - !Ref SSMRole

  SSMRole:
    Type: 'AWS::IAM::Role'
    Properties: 
      AssumeRolePolicyDocument: 
        Version: '2012-10-17'
        Statement: 
          - Effect: Allow
            Principal: 
              Service: 
                - ec2.amazonaws.com
            Action: 
              - sts:AssumeRole
      Path: /
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
      Policies:
        - PolicyName: ListBucketsPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - s3:ListAllMyBuckets
                  - s3:CreateBucket
                  - s3:DeleteBucket
                  - s3:DeleteObject
                  - s3:ListBucket
                  - s3:PutObject
                  - s3:GetObject
                Resource: "*"
Outputs:
  VPCId:
    Description: The VPC ID
    Value: !Ref VPC

  InstanceIdA:
    Description: The Instance ID
    Value: !Ref MyInstanceA

  InstanceIdB:
    Description: The Instance ID
    Value: !Ref MyInstanceB

  PublicSubnetId:
    Description: The Subnet ID
    Value: !Ref PublicSubnet

```

`ec2.yaml`として保存します。
なお、EC2起動と同時にMountpoint for S3のインストールも可能ですが、今回は手動でインストールします。
※Systems ManagerのRun Commandを使ってインストールする方法もありますが、今回は手動でインストールします。

### CloudFormationでスタックを作成

AWSマネジメントコンソールからCloudFormationを開きます。検索画面で`CloudFormation`と入力して`CloudFormation`を選択します。

画面右上の`Create stack`をクリックして`With new resources(standard)`を選択します。
画面のとおりに選択をして、`Choose file`では今回作成したテンプレートを選択します。
スタック名は`Mountpoint-for-S3`とし、`Next`をクリックします。

しばらく似たような画面が続くので全てデフォルトで`Next`をクリックします。
最後の画面ではチェックボックスにチェックを入れて`Next`をクリックします

## EC2（`MyEC2InstanceA`）にMountpoint for S3のインストール

今回はAmazon Linux 2023をOSとする2つのEC2にMountpoint for S3をインストールします。
AWSマネジメントコンソールからEC2を開きます。検索画面で`EC2`と入力して`EC2`を選択します。
まずは、SSMを使ってEC2(`MyEC2InstanceA`)にログインします。`MyEC2InstanceA`にチェックを入れます。

画面右上の`Connect`をクリックします。

`Session Manager`を選択して`Connect`をクリックします。

黒い画面が表示されたら、bashを起動します。

```bash
bash
```

次にデフォルトでは`bin`フォルダがカレントディレクトリになっているため、`cd`コマンドでホームディレクトリに移動します。

```bash
cd
```

以下のコマンドを実行して、Mountpoint for S3をインストールします。

```bash
wget https://s3.amazonaws.com/mountpoint-s3-release/latest/x86_64/mount-s3.rpm
sudo yum install ./mount-s3.rpm
```

実行結果

```text
wget https://s3.amazonaws.com/mountpoint-s3-release/latest/x86_64/mount-s3.rpm
sudo yum install ./mount-s3.rpm
--2024-06-13 12:35:40--  https://s3.amazonaws.com/mountpoint-s3-release/latest/x86_64/mount-s3.rpm
Resolving s3.amazonaws.com (s3.amazonaws.com)... 16.182.105.240, 52.216.208.232, 3.5.30.107, ...
Connecting to s3.amazonaws.com (s3.amazonaws.com)|16.182.105.240|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 11859088 (11M) [binary/octet-stream]
Saving to: ‘mount-s3.rpm’

mount-s3.rpm                                                           100%[==========================================================================================================================================================================>]  11.31M  6.63MB/s    in 1.7s

2024-06-13 12:35:43 (6.63 MB/s) - ‘mount-s3.rpm’ saved [11859088/11859088]

Last metadata expiration check: 0:14:49 ago on Thu Jun 13 12:20:55 2024.
Dependencies resolved.
==========================================================================================================================================================================================================================================================================================
 Package                                                            Architecture                                                  Version                                                                       Repository                                                           Size
==========================================================================================================================================================================================================================================================================================
Installing:
 mount-s3                                                           x86_64                                                        1.7.0-1                                                                       @commandline                                                         11 M
Installing dependencies:
 fuse                                                               x86_64                                                        2.9.9-13.amzn2023.0.2                                                         amazonlinux                                                          80 k
 fuse-common                                                        x86_64                                                        3.10.4-1.amzn2023.0.2                                                         amazonlinux                                                         8.5 k

Transaction Summary
==========================================================================================================================================================================================================================================================================================
Install  3 Packages

Total size: 11 M
Total download size: 88 k
Installed size: 61 M
Is this ok [y/N]: y
Downloading Packages:
(1/2): fuse-common-3.10.4-1.amzn2023.0.2.x86_64.rpm                                                                                                                                                                                                       126 kB/s | 8.5 kB     00:00
(2/2): fuse-2.9.9-13.amzn2023.0.2.x86_64.rpm                                                                                                                                                                                                              1.1 MB/s |  80 kB     00:00
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                                                                                                                                                                     616 kB/s |  88 kB     00:00
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                                                                                                                                                                                                                                  1/1
  Installing       : fuse-common-3.10.4-1.amzn2023.0.2.x86_64                                                                                                                                                                                                                         1/3
  Installing       : fuse-2.9.9-13.amzn2023.0.2.x86_64                                                                                                                                                                                                                                2/3
  Installing       : mount-s3-1.7.0-1.x86_64                                                                                                                                                                                                                                          3/3
  Running scriptlet: mount-s3-1.7.0-1.x86_64                                                                                                                                                                                                                                          3/3
  Verifying        : fuse-2.9.9-13.amzn2023.0.2.x86_64                                                                                                                                                                                                                                1/3
  Verifying        : fuse-common-3.10.4-1.amzn2023.0.2.x86_64                                                                                                                                                                                                                         2/3
  Verifying        : mount-s3-1.7.0-1.x86_64                                                                                                                                                                                                                                          3/3

Installed:
  fuse-2.9.9-13.amzn2023.0.2.x86_64                                                             fuse-common-3.10.4-1.amzn2023.0.2.x86_64                                                             mount-s3-1.7.0-1.x86_64

Complete!
```

## `MyEC2InstanceA`にマウント用のディレクトリを作成する

マウント用のフォルダを作成するために以下のコマンドを実行します。

```bash
mkdir my-bucket
```

## バケットの作成

つぎにマウント先となるS3バケットを作成します。

```bash
export AWS_ACCOUNT_ID=`aws sts get-caller-identity --query 'Account' --output text`
aws s3 mb s3://my-bucket-$AWS_ACCOUNT_ID --region ap-northeast-1
```

## バケットをディレクトリにマウント

以下のコマンドを実行してディレクトリmy-bucketをS3にマウントします。

```bash
mount-s3 --allow-overwrite my-bucket-$AWS_ACCOUNT_ID my-bucket
```

実行結果

```text
[ssm-user@ip-10-0-1-254 ~]$ mount-s3 --allow-overwrite my-bucket-$AWS_ACCOUNT_ID my-bucket
bucket my-bucket-XXXXXX is mounted at my-bucket
```

※XXXXXXには$AWS_ACCOUNT_IDが入ります。

## S3との同期確認

マウントできているかを確認するためになんでもいいのでファイルを作ってS3に同期させてみましょう。
以下のコマンドを実行します。

```bash
echo "Hello, World" > test.txt && mv test.txt my-bucket/test.txt && ls -la my-bucket
```

実行結果

```text
[ssm-user@ip-10-0-1-254 ~]$ echo "Hello, World" > test.txt && mv test.txt my-bucket/test.txt && ls -la my-bucket
total 1
drwxr-xr-x. 2 ssm-user ssm-user  0 Jun 13 12:41 .
drwx------. 3 ssm-user ssm-user 99 Jun 13 12:48 ..
-rw-r--r--. 1 ssm-user ssm-user 13 Jun 13  2024 test.txt
```

ファイルが作成されましたので以下のコマンドを使ってS3に同期できているかをします。

```bash
aws s3 ls my-bucket-$AWS_ACCOUNT_ID
```

実行結果

```text
2024-06-13 12:48:37         13 test.txt
```

ファイルが同期できました。

## EC2（`MyEC2InstanceB`）にMountpoint for S3のインストール

`MyEC2InstanceA`で作ったファイルはS3に同期されました。では次に`MyEC2InstanceB`を使ってS3に同期されたファイルを確認します。
同じ流れでSSMを使ってEC2(`MyEC2InstanceB`)にログインします。`MyEC2InstanceB`にチェックを入れます。

画面右上の`Connect`をクリックします。

`Session Manager`を選択して`Connect`をクリックします。

黒い画面が表示されたら、bashを起動します。

```bash
bash
```

次にデフォルトでは`bin`フォルダがカレントディレクトリになっているため、`cd`コマンドでホームディレクトリに移動します。

```bash
cd
```

以下のコマンドを実行して、Mountpoint for S3をインストールします。

```bash
wget https://s3.amazonaws.com/mountpoint-s3-release/latest/x86_64/mount-s3.rpm
sudo yum install ./mount-s3.rpm
```

※実行結果は省略

## ディレクトリにS3バケットをマウントする

まずは、`MyEC2InstanceB`にマウント用ディレクトリを作成します。

```bash
mkdir my-bucket
```

以下のコマンドを実行してディレクトリmy-bucketをS3にマウントします。

```bash
export AWS_ACCOUNT_ID=`aws sts get-caller-identity --query 'Account' --output text`
mount-s3 --allow-overwrite my-bucket-$AWS_ACCOUNT_ID my-bucket
```

実行結果

```text
bucket my-bucket-XXXXXX is mounted at my-bucket
```

※XXXXXXには$AWS_ACCOUNT_IDが入ります。

## マウントされたディレクトリを確認する

マウントできているかを確認するために以下のコマンドを使ってS3に同期できているかをします。

```bash
ls -la my-bucket
```

実行結果

```text
total 1
drwxr-xr-x. 2 ssm-user ssm-user  0 Jun 13 12:58 .
drwx------. 3 ssm-user ssm-user 99 Jun 13 12:58 ..
-rw-r--r--. 1 ssm-user ssm-user 13 Jun 13 12:48 test.txt
```

ついでにファイルの中身も確認します。

```bash
cat my-bucket/test.txt
```

実行結果

```text
Hello, World
```

これで2つのEC2がひとつのS3バケットを同期するようになりました。

## まとめ

Mountpoint for S3は使いどころを選ぶとかなり良いのものでこれを使えば、S3を保存用ドライブとして扱えるため、よく使うファイルなどを置いておくとEC2からサッと取り出せます。
使い道はとくに決まっていませんが、CodeBuildにおけるアーティファクトの保存先を管理したりすることもできるのかなとふと思いました。

## リソースの削除方法

今回はCloudFormationでやっているため、テンプレートを削除します。その後、作成したS3バケットを削除します。

## おわり
