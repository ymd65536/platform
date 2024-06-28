# セットアップ

## このリポジトリの説明

このリポジトリは、AWSのCodeシリーズを使ったシンプルなCI/CDの構築を目指しています。

## cfnのデプロイ

以下の順番でデプロイします。

```bash
aws cloudformation deploy --stack-name CodeIamRole --template-file CodeIamRole.yml --capabilities CAPABILITY_NAMED_IAM
```

```bash
aws cloudformation deploy --stack-name CodeDevSrc --template-file CodeDevSrc.yml
```

```bash
aws cloudformation deploy --stack-name CodeServices --template-file CodeServices.yml
```
