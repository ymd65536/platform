# devcontainerの使い方

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
