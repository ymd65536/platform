
# 基本コマンド

## AWSのアカウントIDを取得する

```bash
export AWS_ACCOUNT_ID=`aws sts get-caller-identity --query 'Account' --output text` && echo $AWS_ACCOUNT_ID
```

## AWS CLIの設定を見る

```bash
aws configure list
```
