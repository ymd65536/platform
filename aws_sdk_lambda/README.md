# AWS LambdaをAWS SDKで実行する

## 事前準備

まずはどのアカウントで実行するかを確認します。

```bash
export AWS_ACCOUNT_ID=`aws sts get-caller-identity --query 'Account' --output text` && echo $AWS_ACCOUNT_ID
```

## 実行が同期が非同期か

Invokeするときに`InvocationType`で何が指定されているのかで決まる。

[参考:Lambda コンテキストオブジェクトを使用して Python 関数の情報を取得する - AWS Lambda](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-context.html)

同期実行（RequestResponse）の場合

```python
client = boto3.client('lambda')
response = client.invoke(
    FunctionName='YamadaLambda',
    InvocationType='RequestResponse',
    Payload=json.dumps({'key1': 'value1', 'key2': 'value2'})
)
print(response['Payload'].read().decode('utf-8'))

```

非同期実行（Event）の場合

```python
client = boto3.client('lambda')
response = client.invoke(
    FunctionName='YamadaLambda',
    InvocationType='Event',
    Payload=json.dumps({'key1': 'value1', 'key2': 'value2'})
)
print(response['Payload'].read().decode('utf-8'))

```
