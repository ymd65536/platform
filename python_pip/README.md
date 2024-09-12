# Pythonとpipの使い方メモ

## Pythonのバージョン確認

```bash
python --version
```

## pipのバージョン確認

```bash
pip --version
```

## pipのアップグレード

```bash
pip install --upgrade pip
```

## パッケージのインストール

index-urlオプションを指定してインストールする。

```bash
python -m pip install --index-url https://pypi.org/ --user build twine
```

## pip configのTips

global.extra-index-urlとglobal.site-index-urlを設定する。

```bash
pip config set global.extra-index-url ''
pip config set global.site-index-url ''
```

index-urlをpip configで設定する。

```bash
pip config set global.index-url https://pypi.org/simple
```

`ERROR: Can not perform a '--user' install. User site-packages are not visible in this virtualenv.`のエラーが発生するのを防ぐために、ユーザーインストールを無効にします。

```bash
pip config set install.user 'false'
```
