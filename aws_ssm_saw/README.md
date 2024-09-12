# AWS Support Automation Workflows

## はじめに

この記事では「この前リリースされた機能って実際に動かすとどんな感じなんだろう」とか「もしかしたら内容次第では使えるかも？？」などAWSサービスの中でも特定の機能にフォーカスして検証していく記事です。主な内容としては実践したときのメモを中心に書きます。（忘れやすいことなど）
誤りなどがあれば書き直していく予定です。

今回はAWS Systems Managerが機能として提供しているAWS Support Automation Workflowsを検証してみます。

[サポートオートメーションワークフロー（SAW）を使用したAWS環境の一般的な問題の診断](https://aws.amazon.com/jp/blogs/news/using-saw-to-diagnose-common-issues-in-your-aws-environment/)

## AWS Support Automation Workflows（SAW）とは

ではまず、概要をおさらいします。AWS Support Automation Workflows（SAW）とはなんでしょうか。

> AWS のお客様向けのセルフサービス診断と修復
> AWS サポート自動化ワークフローは、厳選された AWS Systems Manager セルフサービス自動化ランブックのコレクションです。これらのランブックは、お客様の問題を解決して得たベストプラクティスを基に、AWS サポートエンジニアリングによって作成されています。これにより、AWS リソースに関する一般的な問題のトラブルシューティング、診断、修正が可能になります。

[AWS Support Automation Workflows（SAW）](https://aws.amazon.com/jp/premiumsupport/technology/saw/)

つまりはトラブルシューティングなどをランブックで実行できるサービスということです。
ランブックのコレクションともありますのでさまざまなランブックを管理して提供する機能ともいえます。

なんともいえないので実際に実行して試してみましょう。

## 環境構築

今回は以下のCloud Fromationテンプレートを使ってEC2を起動します。

```yaml
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

  PublicSubnetId:
    Description: The Subnet ID
    Value: !Ref PublicSubnet
```

## AWS Support Automation Workflowsを開く

[AWS Support Automation Workflowsのリンク](https://ap-northeast-1.console.aws.amazon.com/systems-manager/documents?region=ap-northeast-1)からAWS Support Automation Workflowsを開きます。

なお、AWS Support Automation WorkflowsはAWS Systems Managerの`Document`メニューから確認できます。今回は上記のリンクから直接開きます。

![スクリーンショット 2024-09-10 22.12.30.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/527543/92e439d2-d6e7-468c-1ae2-6da46f5039f1.png)

[AWS Systems Manager - aws](https://ap-northeast-1.console.aws.amazon.com/systems-manager/home?region=ap-northeast-1#)

## ドキュメントを検索する

今回は起動したEC2を止めるため`AWS-StopEC2Instance`というドキュメントを検索します。

![スクリーンショット 2024-09-10 22.13.42.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/527543/6ec208f5-a9ae-ab83-eea5-1270c0590a4d.png)

検索にヒットした`AWS-StopEC2Instance`というリンクをクリックします。

## Automationを実行する

前の画面から画面に遷移するとドキュメントの詳細が表示されます。
Execute automationをクリックします。

![スクリーンショット 2024-09-10 22.15.44.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/527543/c111228f-5214-67e5-8404-a109635b588d.png)

次にどのように実行したらよいか質問されるので順番に設定していきましょう。

まずは実行方法です。
今回は`Simple execution`で実行します。`Simple execution`を選択します。

![スクリーンショット 2024-09-10 22.18.33.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/527543/0b50babc-7344-6b62-0cdd-a043399d399e.png)

Input parameterでは停止予定のインスタンスIDを指定します。

![スクリーンショット 2024-09-10 22.21.44.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/527543/5c267a33-33b0-475a-c228-85e681525844.png)

さまざまな設定項目がありますが、今回はスキップして`Execute`をクリックします。

![スクリーンショット 2024-09-10 22.24.37.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/527543/1256072c-3ba2-599c-6e2a-d73100b3f512.png)

## 実行結果

![スクリーンショット 2024-09-10 22.29.24.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/527543/470dc755-97e0-4892-f2c3-454bf41a96cf.png)

## まとめ

AWS Support Automation Workflowsを利用することによってEC2のマネジメントコンソール以外でEC2を停止することができました。

AWS Support Automation Workflowsは事前に作成されたドキュメントに従ってコマンドを実行します。
内製開発することによってAWS Support Automation Workflowsのドキュメントにはないものも実行可能です。

個人的にはデータのカタログを`データカタログ`と言うようにRunbookのカタログみたいに見えたので
`ランブックカタログ`？みたいなものかなと思いました。

## おわり
