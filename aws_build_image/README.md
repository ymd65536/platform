# 使い方

## アカウントIDの取得

```bash
export AWS_ACCOUNT_ID=`aws sts get-caller-identity --query 'Account' --output text` && echo $AWS_ACCOUNT_ID
```

## ECRへのログイン

```bash
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.ap-northeast-1.amazonaws.com
```

## 引数ありのビルド（新バージョン）

```bash
docker image build --build-arg AWS_ACCOUNT_ID=$AWS_ACCOUNT_ID . -t image-dev
```

## イメージのプル

```bash
docker pull $AWS_ACCOUNT_ID.dkr.ecr.ap-northeast-1.amazonaws.com/image-dev:latest
```

```bash
docker image ls
```
