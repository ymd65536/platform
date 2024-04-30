# Amazon bedrockの基本コマンドメモ

[参考](https://docs.aws.amazon.com/ja_jp/bedrock/latest/userguide/models-supported.html)

## Amazon Bedrock 基盤モデルを一覧表示

```bash
aws bedrock list-foundation-models
```

## v2 Anthropic Claude に関する情報を取得

```bash
aws bedrock get-foundation-model --model-identifier anthropic.claude-v2
```
