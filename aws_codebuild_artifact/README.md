# AWS CodeArtifactをAWS CodeBuildで検証する

## はじめに

AWS CodeArtifactをAWS CodeBuildで検証します。

この記事では「この前リリースされた機能って実際に動かすとどんな感じなんだろう」とか「もしかしたら内容次第では使えるかも？？」などAWSサービスの中でも特定の機能にフォーカスしたり、サービス間連携を検証していく記事です。
主な内容としては実践したときのメモを中心に書きます。（忘れやすいことなど）誤りなどがあれば書き直していく予定です。

今回はAWS CodeBuildでAWS CodeArtifactを使うとどうなるのかを検証します。

## AWSのCodeシリーズとは

AWSには「Code」と名のつくサービスがいくつかあります。いくつか抜粋してみると以下のようなものがあります。

- AWS CodeCommit
- AWS CodeBuild
- AWS CodeDeploy
- AWS CodePipeline
- AWS CodeArtifact
- AWS CodeGuru
- AWS CodeDeploy

Amazon CodeCalystというサービスもありますが、これもCodeシリーズに含まれるのかは不明です。少なくともCodeと名がつくサービスであり、開発者向けのサービスとして提供されています。なお、CodeStarについては2024年7月31日をもってサポートが終了となります。

## 今回使うサービス

コードシリーズの全体像がみえたところで、「CodeArtifact」と「CodeBuild」はどんなサービスでしょうか。

### AWS CodeArtifact

AWS CodeArtifactはパッケージマネージャツール(Maven、Gradle、npm、Yarn、Twine、pip、NuGetなど)でダウンロードするパッケージを管理するサービスです。

AWSのドキュメントでは以下のように説明されています。

ソフトウェア開発のためのセキュアかつスケーラブルでコスト効率性に優れたパッケージ管理

CodeArtifact を使用すると、一般的なパッケージマネージャーを使用してアーティファクトを格納し、Maven、Gradle、npm、Yarn、Twine、pip、NuGet などのツールを構築できます。CodeArtifact は、パブリックパッケージリポジトリからオンデマンドでソフトウェアパッケージを自動的にフェッチできるため、アプリケーションの依存関係の最新バージョンにアクセスできます。

よくわからない方は以下の記事を参考にしてください。

[ハンズオン](https://qiita.com/ymd65536/items/4b1c9ddf0b1280d39883)

## AWS CodeBuild

AWSではビルド環境を提供してくれるサービスがあります。それがAWS CodeBuildです。
AWS CodeBuildは`buildspec.yml`というAWS CodeBuild特有の設定ファイルからビルド設定を読み取り、ビルドを自動化します。
また、ビルドはビルドプロジェクトという単位で管理され、ブランチ単位とコミットID単位でビルドできます。

```yaml
version: 0.2
phases:
  install:
    on-failure: ABORT
    commands:
      - echo "install phases"
  pre_build:
    on-failure: ABORT
    commands:
      - echo "pre_build phases"
  build:
    on-failure: ABORT
    commands:
      - echo "build phases"
  post_build:
    on-failure: ABORT
    commands:
      - echo "post_build phases"
artifacts:
  files:
    - "**/*"

```

なお、ビルド時に環境変数を呼び出すことが可能であり、環境変数はymlファイル内に埋め込むことができます。
環境変数におくデータは以下の3つの形式で保存できます。

- PlainText
- Systems Manager Parameter Store
- Secret Manager

さらにビルド状況を監視する為にCloudWatchを利用してビルド時のログを参照することもできます。
※ビルドプロジェクトが非VPCの場合はそのまま利用できますが、VPCの場合は別途、設定が必要です。

ビルドのソースはAWS CodeCommitだけでなく他のリポジトリサービスも利用できます。

## CodeArtifactとCodeBuildの関係

簡単に説明すると、CodeArtifactはパッケージ管理サービスであり、CodeBuildはビルド環境を提供するサービスです。
CodeArtifactで管理されているパッケージはCodeBuildで利用できます。

通常、CodeBuildでソフトウェアパッケージをインストールする場合
パブリックで公開されているパッケージレジストリからパッケージをダウンロードするためにインターネットにアクセスする必要がありますが、CodeArtifactを利用することによってAWS内のパッケージレジストリからパッケージをダウンロードできます。
つまりインターネットを抜けることなくAWSで完結できます。

## ハンズオン（おおまかな流れ）

おおまかな流れを紹介します。

まずはCodeArtifactをセットアップします。そのあとCodeBuildをセットします。

CodeArtifactのセットアップは以下の手順で行います。

1. CodeArtifactのドメインの作成
2. CodeArtifactのリポジトリの作成
3. npm-storeを作成
4. リポジトリとnpm-store を接続する
5. CodeArtifactにログイン
6. エンドポイントURLの取得とCODEARTIFACT_AUTH_TOKENの発行
7. yarnの設定
8. パッケージを登録

CodeBuildのセットアップは以下の手順で行います。

1. CloudFormationでCodeCommitのスタックを作成
2. CodeCommitの設定
3. CloudFormationでCodeBuildのスタックを作成
4. CloudFormationでCodePipelineのスタックを作成
5. 実行結果の確認
