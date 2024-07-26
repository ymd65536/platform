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
aws ecs register-task-definition --cli-input-json ./ecs/task-definition.json
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
aws ecs list-tasks --cluster simple-ecs-cluster --service-name simple-ecs-service
```

## Systems Manager Session Managerを使ってSSH接続する

```bash
aws ecs execute-command --region ap-northeast-1 --cluster simple-ecs-cluster --task タスクID --container template-image --interactive --command "/bin/sh"
```
