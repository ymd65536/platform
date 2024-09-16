# devcontainerの使い方

## devcontainer.jsonの設定

Rancher-Desktopと組み合わせて利用するときは以下の2点に注意してください。

- `Dev › Containers: Docker Socket Path`を絶対パスで指定する
- `Dev › Containers: Docker Path`のパスを絶対パスで設定する

`Dev › Containers: Docker Path`のパスが指定が良くない場合は`Docker version 17.12.0 or later required`と表示されます。

[Rancher-Desktop](https://rancherdesktop.io/)
[Rancher-Desktop - GitHub](https://github.com/rancher-sandbox/rancher-desktop)

## typescript-node

```json
{
    "image": "mcr.microsoft.com/devcontainers/typescript-node",
    "forwardPorts": [
        3000
    ],
    "customizations": {
        // Configure properties specific to VS Code.
        "vscode": {
            // Add the IDs of extensions you want installed when the container is created.
            "extensions": []
        }
    }
}
```

## dockerfileをベースに環境を作成する

```json
{
    "name": "Dockerfile",
    "build": { "dockerfile": "dockerfile" },
    "forwardPorts": [
        3000
    ],
    "customizations": {
        // Configure properties specific to VS Code.
        "vscode": {
            // Add the IDs of extensions you want installed when the container is created.
            "extensions": []
        }
    }
}
```

## dockerのTips

`<none>`タグのイメージを削除する

```bash
docker rmi $(docker images -f "dangling=true" -q)
```

## Amazon Linux 2023イメージについて

[AL2023 最小コンテナイメージ - amazon user guide](https://docs.aws.amazon.com/ja_jp/linux/al2023/ug/minimal-container.html)

awscliをzipでインストールしたら以下のエラーが発生した。
※awscliのインストール方法: [リンク](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

```text
Cannot uninstall Pygments 2.7.4, RECORD file not found
```

dnfではなくpipでインストールするとエラーは発生しない。

Pygmentsについては以下のリンクを参照してください。

- [Pygments](https://pygments.org/)

## 参考

- [Developing inside a Container](https://code.visualstudio.com/docs/devcontainers/containers#_create-a-devcontainerjson-file)
- [Add another local file mount](https://code.visualstudio.com/remote/advancedcontainers/add-local-file-mount)
- [Alternate ways to install Docker](https://code.visualstudio.com/remote/advancedcontainers/docker-options)
- [Create a Dev Container](https://code.visualstudio.com/docs/devcontainers/create-dev-container)

## devcontainerに使うコンテナイメージについて

実際にdevcontainerを使ってみて、開発に使うコンテナイメージの選定には気をつけないといけません。
選定をする際のポイントは以下の通りです。

- どんなコマンドを実行するか
- どんなライブラリ/パッケージを使うか
- どのような環境と連携するか

他にも以下のようなポイントがありますが、今回は扱いません。

- セキュリティ
- コンテナイメージのサイズ
- メンテナンス（コンテナイメージのサポート期間やバージョン管理）

では、実際にポイントを見ていきましょう。

## どんなコマンドを実行するか

devcontainer上で実行するコマンドによって、コンテナイメージを選定する必要があります。
たとえば、AWS CDKを使う場合はNode.jsをインストールされているコンテナイメージか
あるいはNode.jsをインストールできるコンテナイメージを選定する必要があります。

Node.jsをインストールできるコンテナイメージを選定する場合は
どのパッケージマネージャを使うかどうかも考慮する必要があります。
たとえば、debian系なら`apt-get`、RedHat系なら`yum`、`dnf`、`rpm`などを使った方法があります。

他にもAWS CLIを使う場合はさまざまな方法でインストールできるため、どの方法を利用してインストールするか選定する必要があります。

### AWS CDKを使う場合

AWS CDKを使う場合はNode.jsをインストールできるコンテナイメージを選定する必要があります。

### AWS CLIを使う場合

AWS CLIを使う場合はさまざまな方法でインストールできるため、どの方法を利用してインストールするか選定する必要があります。

### dockerを使う場合

`mcr.microsoft.com/devcontainers/typescript-node`を使うと良いでしょう。
