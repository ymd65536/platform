# メモ

## 概要

「よく使うコマンドや設定をメモしておくとプラットフォームエンジニアリングにつながりやすい。」
ということからよく使うコマンドや設定をメモしておくリポジトリです。

もはや、ツールセットみたいになっています。

## フォルダの説明

|項番|フォルダ名|説明|
|:--:|:--|:--|
|1|awscli|AWS CLIの使い方|
|2|aws_amplify|AWS Amplifyの使い方|
|3|aws_build_image|AWSでDockerイメージをビルドするインフラ構成|
|4|aws_codebuild_artifact|AWS CodeArtifactの使い方|
|5|aws_codebuild_exe_lambda|Lambdaでイメージをビルドする|
|6|aws_simple_cicd|AWSでシンプルなCI/CDを構築する|
|7|aws_simple_ecs|AWSでシンプルなECSを構築する|
|8|chrome_extensions|Chrome拡張機能の使い方|
|9|ec2_template|EC2を起動するためのCloudFormationテンプレート|
|10|javascript_fetch_api|JavaScriptでFetch APIを使うサンプル|
|11|Momento|（作成中）|
|12|Mountpoint_for_S3|Mountpoint for S3を使ってEC2にS3バケットをマウントする|
|13|php-docker|dockerでphpを動かす|
|14|py_build_toml|tomlファイルを使ってPythonのパッケージをビルドする|
|15|py_jinja2|FlaskでJinja2を使うサンプル|
|16|test_nginx|nginxのテスト|
|17|flask_blog_app|Flaskでブログアプリを作成する|

## Dev ContainerのpostCreateCommand.shのセットアップ

Dev Containerではユーザーフォルダにある`postCreateCommand.sh`を利用しています。

`postCreateCommand.sh`では以下の設定を行っています。

```bash
# /bin/bash
clear
git config --global user.name "{github username}"
git config --global user.email "{github email}"
git config --global user.name && git config --global user.email
```

## トラブルシューティング

`git push`で`SSL certificate problem: self signed certificate in certificate chain`が出る場合は
以下のコマンドを実行して、証明書を追加してください。

```bash
git config --global http.sslCAInfo ~/SSL-TrustCA.crt
```
