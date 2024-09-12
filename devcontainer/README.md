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
