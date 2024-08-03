# nginxをCodeBuildでビルドするサンプル

## 概要

このリポジトリは、CodeBuildでnginxをビルドするサンプルです。

## ファイル構成

```text
test_nginx/
├── buildspec.yml
├── Dockerfile
└── README.md
```

### ファイル説明

- `buildspec.yml`: CodeBuildのビルド仕様ファイル
- `Dockerfile`: nginxのビルド定義ファイル
- `README.md`: このファイル
- `index.html`: nginxが配信するHTMLファイル
- `nginx.conf`: nginxの設定ファイル
- `test.sh`: テストスクリプト
