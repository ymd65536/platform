# AWS CDKのメモ

## AWS CDKとは

- AWS Cloud Development Kit
- AWSのリソースをコードで管理するためのフレームワーク
- TypeScript, Python, Java, C# で記述可能

## AWS docs

- [AWS CDK スタック](https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/stacks.html)
- [リソースと AWS CDK](https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/resources.html)

## 公式リファレンス

### class

- [CfnEIP](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.CfnEIP.html)
- [Vpc](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.Vpc.html)
- [Subnet](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.Subnet.html)
- [CfnNatGateway](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.CfnNatGateway.html)

### interface

- [VpcLookupOptions](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.VpcLookupOptions.html)

## その他

- [AWS CDKでNAT GatewayにEIPを割り当てる方法](https://qiita.com/reoring/items/4577de0bf63a9f787339)
- [CDKを使ったときの問題と対応](https://qiita.com/dmikita/items/f1dd6d6ad0a837d6f5fa)

## ハマりどころ

- cdk.context.jsonについて

### cdk.context.jsonについて

- デプロイ時に利用するパラメータを記述するファイル

構成を変更したら、`cdk.context.json`を削除してからcdk deployすること。これをやらないと古いパラメータを元にスタックを作成しようと試みるため、エラーが発生する。
