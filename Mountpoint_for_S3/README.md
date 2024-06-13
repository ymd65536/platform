


# 手を動かして学ぶMountpoint for S3

## はじめに

この記事ではMountpoint for S3を使って、EC2にS3バケットをマウントする触る話を書きます。
主な内容としては実践したときのメモを中心に書きます。（忘れやすいことなど）
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

  InstanceId:
    Description: The Instance ID
    Value: !Ref MyInstance

  PublicSubnetId:
    Description: The Subnet ID
    Value: !Ref PublicSubnet

```

`ec2.yaml`として保存します。
なお、EC2起動と同時にMountpoint for S3のインストールも可能ですが、今回は手動でインストールします。
※Systems ManagerのRun Commandを使ってインストールする方法もありますが、今回は手動でインストールします。

### CloudFormationでスタックを作成

AWSマネジメントコンソールからCloudFormationを開きます。検索画面で`CloudFormation`と入力して`CloudFormation`を選択します。

![Screenshot 2024-06-13 at 21.14.12.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/527543/9fc4abab-e46a-021d-b614-b1f349b16434.png)

画面右上の`Create stack`をクリックして`With new resources(standard)`を選択します。

![Screenshot 2024-06-13 at 21.15.01.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/527543/70fdf3c7-fd94-2ddd-fe79-878bfd8f29f7.png)

画面のとおりに選択をして、`Choose file`では今回作成したテンプレートを選択します。

![Screenshot 2024-06-13 at 21.15.44.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/527543/a507e164-9051-fa38-9705-e472be1c3e1b.png)

スタック名は`Mountpoint-for-S3`とし、`Next`をクリックします。

![Screenshot 2024-06-13 at 21.17.08.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/527543/f0b775f1-ad90-c4ad-446e-d44bfc3ec3d7.png)

しばらく似たような画面が続くので全てデフォルトで`Next`をクリックします。
最後の画面ではチェックボックスにチェックを入れて`Next`をクリックします

![Screenshot 2024-06-13 at 21.18.12.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/527543/b8a7817d-7605-a96a-99d4-beaf7ea374af.png)

## 2つのEC2にMountpoint for S3のインストール

今回はAmazon Linux 2023をOSとする2つのEC2にMountpoint for S3をインストールします。

まずは、SSMを使ってEC2()にログインします。黒い画面が表示されたら、bashを起動します。

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

## バケットの作成

```bash
aws s3 mb s3://my-bucket-$AWS_ACCOUNT_ID --region ap-northeast-1
```

```bash
export AWS_ACCOUNT_ID=`aws sts get-caller-identity --query 'Account' --output text`
mkdir my-bucket
mount-s3 --allow-overwrite my-bucket-$AWS_ACCOUNT_ID my-bucket -- -o nonempty
```

## Test

```bash
echo "Hello, World" > test.txt && mv test.txt my-bucket/test.txt
```

書き込みはできない。（マウント時にオプションが必要）
[file-system-configuration](https://github.com/awslabs/mountpoint-s3/blob/main/doc/CONFIGURATION.md#file-system-configuration)

```bash
echo "Hello, World!" > my-bucket/test.txt
```

```bash
umount ./my-bucket
```

```bash
ls -la my-bucket
```
