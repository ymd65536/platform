
# AWS Amplify

## Install the Amplify CLI

```bash
npm install -g @aws-amplify/cli
```

## Configure the Amplify CLI

IAMユーザーのアクセスキーとシークレットキーを使って設定する場合は以下のコマンドを実行する。

```bash
amplify configure
```

SSOの場合は`.aws/config`にプロファイルを追記する。

## Add Authentication Configuration

`~/.aws/config`を追記する。追記場所は`output=json`の下に追記する。`my-sso-profile`はプロファイル名に置き換える。

```bash
credential_process = aws configure export-credentials --profile my-sso-profile
```

```bash
amplify init
```
