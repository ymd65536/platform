# devcontainerの使い方

## devcontainer.jsonの設定

Rancher-Desktopと組み合わせて利用するときは以下の2点に注意してください。

- `Dev › Containers: Docker Socket Path`を絶対パスで指定する
- `Dev › Containers: Docker Path`のパスを絶対パスで設定する

`Dev › Containers: Docker Path`のパスが指定が良くない場合は`Docker version 17.12.0 or later required`と表示されます。

[Rancher-Desktop](https://rancherdesktop.io/)
[Rancher-Desktop - GitHub](https://github.com/rancher-sandbox/rancher-desktop)

## Amazon Linux 2023イメージを使う

```dockerfile
FROM public.ecr.aws/ubuntu/ubuntu:24.04_stable
RUN apt install python3-pip python3 -y && pip install awscli && curl https://get.volta.sh | bash && RUN /root/.volta/bin/volta install node@18
```

```dockerfile
FROM public.ecr.aws/amazonlinux/amazonlinux:2023-minimal
RUN dnf install -y git tar gzip unzip python3 python3-pip docker && pip install awscli pip==21.3.1 && pip install --force-reinstall build twine && curl https://get.volta.sh | bash && /root/.volta/bin/volta install node@18
```

```json
{
    "name": "deploy-container",
    "build": { "dockerfile": "dockerfile" },
    "customizations": {
        // Configure properties specific to VS Code.
        "vscode": {
            // Add the IDs of extensions you want installed when the container is created.
            "extensions": []
            
        }
    },
    "features": {
        "ghcr.io/devcontainers/features/docker-in-docker:2": {
            "version": "latest",
            "moby": true
        }
    },
    "mounts": [
        "source=${localEnv:HOME}/.aws,target=/root/.aws,type=bind"
    ],
    "postCreateCommand": "npm install -g aws-cdk@2.153.0"
}
```

```json
{
    "name": "Docker in Docker",
    "dockerFile": "Dockerfile",
    "runArgs": [
        "--init",
        "--privileged"
    ],
    "features": {
        "ghcr.io/devcontainers/features/docker-outside-of-docker:1": {}
    },
    "customizations": {
        "vscode": {
        }
    },
    "mounts": [
        "source=${localEnv:HOME}/.aws,target=/home/node/.aws,type=bind",
        "source=${localEnv:HOME}/.docker,target=/home/node/.docker,type=bind"
    ],
    "postCreateCommand": "npm install -g aws-cdk@2.153.0"
}
```

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

## outside of docker

[outside of docker](https://github.com/devcontainers/features/tree/main/src/docker-outside-of-docker)

[typescript-node](https://mcr.microsoft.com/en-us/product/devcontainers/typescript-node/tags)
