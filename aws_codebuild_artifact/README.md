## はじめに

この記事では「この前リリースされた機能って実際に動かすとどんな感じなんだろう」とか「もしかしたら内容次第では使えるかも？？」などAWSサービスの中でも特定の機能にフォーカスしたり、サービス間連携を検証していく記事です。
主な内容としては実践したときのメモを中心に書きます。（忘れやすいことなど）誤りなどがあれば書き直していく予定です。

今回はAWS CodeBuildでAWS CodeArtifactを使うとどうなるのかを検証するために環境をセットアップします。

## そもそもAWSのCodeシリーズとは

AWSには「Code」と名のつくサービスがいくつかあります。いくつか抜粋してみると以下のようなものがあります。

- AWS CodeCommit
- AWS CodeBuild
- AWS CodeDeploy
- AWS CodePipeline
- AWS CodeArtifact
- AWS CodeGuru
- AWS CodeDeploy

Amazon CodeCalystというサービスもありますが、これもCodeシリーズに含まれるのかは不明です。少なくともCodeと名がつくサービスであり、開発者向けのサービスとして提供されています。なお、CodeStarについては2024年7月31日をもってサポートが終了となります。

## 今回扱うサービス

Codeシリーズの全体像がみえたところで、「CodeArtifact」と「CodeBuild」はどんなサービスでしょうか。

### AWS CodeArtifact

AWS CodeArtifactはパッケージマネージャツール(Maven、Gradle、npm、Yarn、Twine、pip、NuGetなど)でダウンロードするパッケージを管理するサービスです。

AWSのドキュメントでは以下のように説明されています。

> ソフトウェア開発のためのセキュアかつスケーラブルでコスト効率性に優れたパッケージ管理

> CodeArtifact を使用すると、一般的なパッケージマネージャーを使用してアーティファクトを格納し、Maven、Gradle、npm、Yarn、Twine、pip、NuGet などのツールを構築できます。CodeArtifact は、パブリックパッケージリポジトリからオンデマンドでソフトウェアパッケージを自動的にフェッチできるため、アプリケーションの依存関係の最新バージョンにアクセスできます。

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

## AWS CodeArtifactのセットアップ

AWS CloudShellを利用してCodeArtifactのセットアップを行います。
AWSマネジメントコンソールを開いて赤枠のターミナルボタンをクリックします。

![Screenshot 2024-06-14 at 19.58.52.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/527543/9a02c3a6-1a2a-3d5a-490e-d49e558633d2.png)

### 環境変数の設定

環境構築に必要な変数を設定します。

|変数名|説明|
|:---|:---|
|AWS_DOMAIN|CodeArtifactのドメイン名|
|REPOSITORY_NAME|リポジトリ名|
|AWS_ACCOUNT_ID|AWSのアカウントID|
|AWS_DEFAULT_REGION|リージョン名|

```bash
export AWS_DOMAIN="cf-handson-domain" && echo $AWS_DOMAIN
export REPOSITORY_NAME="cfhandson"
export AWS_ACCOUNT_ID=`aws sts get-caller-identity --query 'Account' --output text` && echo $AWS_ACCOUNT_ID
export AWS_DEFAULT_REGION="ap-northeast-1" && echo $AWS_DEFAULT_REGION
```

### ドメインの作成

CodeArtifactのドメインを作成します。

```bash
aws codeartifact create-domain --domain $AWS_DOMAIN
```

### リポジトリを作成する

ドメインではパッケージを格納できないため、リポジトリを作成します。

```sh
aws codeartifact create-repository --domain $AWS_DOMAIN --domain-owner $AWS_ACCOUNT_ID --repository $REPOSITORY_NAME
```

### npm-storeを作成する

リポジトリにはnpmのパッケージをいれたいため、まずはnpm-storeを作成します。

```sh
aws codeartifact create-repository --domain $AWS_DOMAIN --domain-owner $AWS_ACCOUNT_ID --repository npm-store
```

### リポジトリとnpm-store を接続する

npm-storeを作成したあとはリポジトリとnpm-storeを接続します。

```sh
aws codeartifact associate-external-connection --domain $AWS_DOMAIN  --domain-owner $AWS_ACCOUNT_ID --repository npm-store --external-connection "public:npmjs"
```

### リポジトリを更新する

最後にリポジトリを更新します。

```sh
aws codeartifact update-repository --repository $REPOSITORY_NAME --domain $AWS_DOMAIN  --domain-owner $AWS_ACCOUNT_ID --upstreams repositoryName=npm-store
```

### CodeArtifactにログイン

エンドポイントの取得やトークンの取得が必要となる為、CodeArtifactににログインします。

```sh
aws codeartifact login --tool npm --domain $AWS_DOMAIN --region $AWS_DEFAULT_REGION --domain-owner $AWS_ACCOUNT_ID --repository $REPOSITORY_NAME
```

### エンドポイントURLの取得とCODEARTIFACT_AUTH_TOKENの発行

CodeArtifactのエンドポイントURLと`CODEARTIFACT_AUTH_TOKEN`を取得します。

```sh
export CODEARTIFACT_URL=`aws codeartifact get-repository-endpoint --domain $AWS_DOMAIN --domain-owner $AWS_ACCOUNT_ID --repository $REPOSITORY_NAME --format npm` && echo $CODEARTIFACT_URL
export CODEARTIFACT_AUTH_TOKEN=`aws codeartifact get-authorization-token --domain $AWS_DOMAIN --region $AWS_DEFAULT_REGION --domain-owner $AWS_ACCOUNT_ID --query authorizationToken --output text` && echo $CODEARTIFACT_AUTH_TOKEN
```

### yarnの設定

CodeArtifactとパッケージマネージャを接続する為にyarnの設定を変更します。

まずはインストールを実行します。

```bash
sudo npm install -g yarn
```

CodeArtifactの設定をyarnに設定します。

```sh
yarn config set npmRegistryServer "$CODEARTIFACT_URL"
yarn config set 'npmRegistries["$CODEARTIFACT_URL"].npmAuthToken' "${CODEARTIFACT_AUTH_TOKEN}"
yarn config set 'npmRegistries["$CODEARTIFACT_URL"].npmAlwaysAuth' "true"
```

### パッケージを登録

CodeArtifactにパッケージが登録されていないことを確認します。

```sh
aws codeartifact list-packages --domain $AWS_DOMAIN --repository $REPOSITORY_NAME --query 'packages' --output text
```

## リポジトリをクローンする

今回使うリポジトリをクローンします。

```bash
git clone https://github.com/ymd65536/aws_codebuild_artifact.git && cd aws_codebuild_artifact
```

## パッケージをCodeArtifactに登録する

`sample-package`のディレクトリに移動します。

```sh
cd ./sample-package
```

CodeArtifactにパッケージを登録します。

```sh
npm publish
```

登録されたパッケージの一覧を表示します。

```sh
aws codeartifact list-packages --domain $AWS_DOMAIN --repository $REPOSITORY_NAME
```

### CodeArtifactに登録したパッケージをsample-appに読み込む

サンプルアプリケーションの`sample-app`に作成したパッケージを読み込みます。

```sh
cd ../sample-app
```

`npm install`を実行して`index.js`を実行します。

```sh
npm install sample-package@1.0.0 && node index.js
```

無事にアプリケーションからパッケージを読み込むことができましたら、CodeArtifactのセットアップは完了です。

## CodeArtifactと連携させる環境のセットアップ

AWS CloudFormationを利用して環境をセットアップを行います。操作はこのままCloudShellで行います。
ディレクトリを移動します。

```sh
cd ../cfn
```

## CodeCommitのセットアップ

### CloudFormationでCodeCommitのスタックを作成

CodeCommitでリポジトリを作成するためにスタックを作成します。以下のコマンドを実行します。

```sh
aws cloudformation deploy --stack-name codecommit --template-file ./codecommit.yml --tags Name=Qiita
```

### CodeCommitの設定

ディレクトリを変更してCodeCommitのリポジトリをクローンします。まずはディレクトリを変更します。

```bash
cd
```

CodeCommitのリポジトリをクローンしてブランチを切ります。

```bash
git clone codecommit::ap-northeast-1://Qiita && cd Qiita
git checkout -b main
```

リポジトリにファイルを追加してコミットしてプッシュします。

```bash
git config --global user.email "you@example.com"
git config --global user.name "ymd65536"
echo "Hello CodeBuild" > README.md
git add .
git commit -m "Qiita"
git push --set-upstream origin main
```

次に`code_build_handson`ブランチを作成してコミットしてプッシュします。

```bash
git checkout -b code_build_handson
git push --set-upstream origin code_build_handson
```

`codecommit`ディレクトリに移動してファイルをコピーしてコミットしてプッシュします。

```bash
cp ../aws_codebuild_artifact/codecommit/* .
git add .
git commit -m "Qiita"
git push
```

## AWS CodeBuildのセットアップ

次にCodeBuildのセットアップを行います。忘れずに以下のコマンドを実行します。

```bash
cd ../aws_codebuild_artifact/cfn/
```

### CloudFormationでCodeBuildのスタックを作成

まずはビルドアーティファクトを格納するS3バケットを作成します。

```bash
aws cloudformation deploy --stack-name s3 --template-file ./s3.yml --tags Name=Qiita --capabilities CAPABILITY_NAMED_IAM
```

次にIAMロールを作成します。

```bash
aws cloudformation deploy --stack-name codebuild-role --template-file ./codebuild-role.yml --tags Name=Qiita --capabilities CAPABILITY_NAMED_IAM
```

CodePipelineのIAMロールも作成します。

```bash
aws cloudformation deploy --stack-name codepipeline-role --template-file ./pipeline-iam-role.yml --tags Name=Qiita --capabilities CAPABILITY_NAMED_IAM
```

最後にCodeBuildのスタックを作成します。

```bash
aws cloudformation deploy --stack-name codebuild --template-file ./codebuild.yml --tags Name=Qiita
```

## CodePipelineのセットアップ

### CloudFormationでCodePipelineのスタックを作成

IAMロールを作成します。

```bash
aws cloudformation deploy --stack-name event-bridge-iam-role --template-file ./event-bridge-iam-role.yml --tags Name=Qiita --capabilities CAPABILITY_NAMED_IAM
```

CodePipelineのスタックを作成します。

```bash
aws cloudformation deploy --stack-name pipeline --template-file ./pipeline.yml --tags Name=Qiita
```

以上でCodePipelineのセットアップは完了です。

## CodePipelineが正常に動作しているか確認する

AWS マネジメントコンソールを開き、CodePiplineを開きます。

![Screenshot 2024-06-14 at 20.10.45.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/527543/9ddf179c-7e8f-06e8-c79d-5405be8ca14d.png)

画面左メニューから`Pipelines`をクリックします。

![Screenshot 2024-06-14 at 20.12.34.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/527543/19deee0a-7403-b8f2-7e78-4bacc8027423.png)

以下のように`Succeeded`となっていれば正常に動作しています。

![Screenshot 2024-06-14 at 20.14.43.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/527543/f62a88bf-ce5d-d103-427b-14658e1e197e.png)

## 次のステップ

長くなりそうなので具体的な実装は次の記事で掲載します。次はCodeBuildからCodeArtifactを引用してパッケージをインストールします。

## いったんおわり
