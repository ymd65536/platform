# シンプルにECSを起動したい

## 概要

ECSを使ってコンテナを起動するための最小限の設定を行います。
このフォルダでできることとしては最小限のLinux環境をコンテナで起動することです。

また、ECSのコンテナに対してはSystems Manager Session Managerを使ってSSHを接続します。

## 前提

- AWS CLIがインストールされていること
- AWS CLIの設定が完了していること
- Dockerがインストールされていること
  - Rancher Desktopを使っていること

## 事前準備

### 1. Dockerイメージをビルドする

```bash
cd src
```

```bash
docker build -t template-image .
```

### 2. DockerイメージをECRにプッシュする

```bash
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text) && echo $AWS_ACCOUNT_ID
aws ecr create-repository --repository-name template-image
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.ap-northeast-1.amazonaws.com
docker tag template-image:latest $AWS_ACCOUNT_ID.dkr.ecr.ap-northeast-1.amazonaws.com/template-image:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.ap-northeast-1.amazonaws.com/template-image:latest
```

## ECS

1. ECSクラスタを作成する
2. ECSタスク定義を作成する
3. ECSサービスを作成する
4. Systems Manager Session Managerを使ってSSH接続する

### 1. ECSクラスタを作成する

```bash
aws ecs create-cluster --cluster-name simple-ecs-cluster
```

### 2. ECSタスク定義を作成する

```bash
aws ecs register-task-definition --cli-input-json file://ecs/task-definition.json
```

`file://`をつけないとフォーマットエラーが返される。

```text
Error parsing parameter 'cli-input-json': Invalid JSON received.
```

### 3. ECSサービスを作成する

```bash
aws ecs create-service --cluster simple-ecs-cluster --service-name simple-ecs-service --task-definition template-image --desired-count 1
```

### 4. Systems Manager Session Managerを使ってSSH接続する

[AWS CLI 用の Session Manager プラグインをインストールする](https://docs.aws.amazon.com/ja_jp/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html)

### Mac M1の場合

```bash
curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/mac_arm64/sessionmanager-bundle.zip" -o "sessionmanager-bundle.zip"
unzip sessionmanager-bundle.zip
```

```bash
sudo ./sessionmanager-bundle/install -i /usr/local/sessionmanagerplugin -b /usr/local/bin/session-manager-plugin
```

```bash
session-manager-plugin
```

### ECSサービス更新

```bash
aws ecs update-service --region ap-northeast-1 --cluster simple-ecs-cluster --service simple-ecs-service --enable-execute-command
```

※ Systems Manager Session Managerを使ってSSH接続するためには、タスクの再起動が必要です。

### ECSタスクのIDを取得する

```bash
aws ecs list-tasks --cluster simple-ecs-cluster --service-name dev-nginx-yamada
```

## Systems Manager Session Managerを使ってSSH接続する

```bash
aws ecs describe-services --cluster simple-ecs-cluster --services dev-nginx-yamada | grep enableExecuteCommand
```

```bash
aws ecs update-service --cluster simple-ecs-cluster --service dev-nginx-yamada --enable-execute-command | grep enableExecuteCommand
```

```bash
aws ecs execute-command --cluster simple-ecs-cluster --task e40860c2b55a4200b03c3197f6c59714 --container dev-yamada --interactive --command "/bin/sh"
```

## Tips

### Troubleshoot Amazon ECS Exec issues

Amazon ECS Exec Checkerを使うとトラブルシューティングが捗る。

[Amazon ECS Exec Checker - GitHub](https://github.com/aws-containers/amazon-ecs-exec-checker)

- [Troubleshoot Amazon ECS Exec issues](https://docs.amazonaws.cn/en_us/AmazonECS/latest/developerguide/ecs-exec-troubleshooting.html)
- [Monitor Amazon ECS containers with ECS Exec](https://docs.amazonaws.cn/en_us/AmazonECS/latest/developerguide/ecs-exec.html#ecs-exec-enabling-and-using)

実行結果の例

```text
amazon-ecs-exec-checker $ ./check-ecs-exec.sh simple-ecs-cluster 43a3aa9f04624160b8410f0594f95015
-------------------------------------------------------------
Prerequisites for check-ecs-exec.sh v0.7
-------------------------------------------------------------
  jq      | OK (/opt/homebrew/bin/jq)
  AWS CLI | OK (/opt/homebrew/bin/aws)

-------------------------------------------------------------
Prerequisites for the AWS CLI to use ECS Exec
-------------------------------------------------------------
  AWS CLI Version        | OK (aws-cli/2.17.14 Python/3.11.9 Darwin/23.5.0 source/arm64)
  Session Manager Plugin | OK (1.2.463.0)

-------------------------------------------------------------
Checks on ECS task and other resources
-------------------------------------------------------------
Region : ap-northeast-1
Cluster: simple-ecs-cluster
Task   : 43a3aa9f04624160b8410f0594f95015
-------------------------------------------------------------
  Cluster Configuration  | Audit Logging Not Configured
  Can I ExecuteCommand?  | arn:aws:iam::123456789012:user/yamada
     ecs:ExecuteCommand: allowed
     ssm:StartSession denied?: allowed
  Task Status            | RUNNING
  Launch Type            | Fargate
  Platform Version       | 1.4.0
  Exec Enabled for Task  | OK
  Container-Level Checks | 
    ----------
      Managed Agent Status
    ----------
         1. RUNNING for "dev-yamada"
    ----------
      Init Process Enabled (dev-yamada:3)
    ----------
         1. Disabled - "dev-yamada"
    ----------
      Read-Only Root Filesystem (dev-yamada:3)
    ----------
         1. Disabled - "dev-yamada"
  Task Role Permissions  | arn:aws:iam::123456789012:role/ecs-task-role
     ssmmessages:CreateControlChannel: allowed
     ssmmessages:CreateDataChannel: allowed
     ssmmessages:OpenControlChannel: allowed
     ssmmessages:OpenDataChannel: allowed
  VPC Endpoints          | 
    Found existing endpoints for vpc-XXXXX:
      - com.amazonaws.vpce.ap-northeast-1.vpce-svc-XXXXX
    SSM PrivateLink "com.amazonaws.ap-northeast-1.ssmmessages" not found. You must ensure your task has proper outbound internet connectivity.  Environment Variables  | (dev-yamada:3)
       1. container "dev-yamada"
       - AWS_ACCESS_KEY: not defined
       - AWS_ACCESS_KEY_ID: not defined
       - AWS_SECRET_ACCESS_KEY: not defined
```
