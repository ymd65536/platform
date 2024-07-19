# py_build_toml

Pythonのビルド環境を構築するための設定ファイルを作成します。

## Pythonのbuildをインストール

```bash
python -m pip install --upgrade build
```

## パッケージをビルドしてインストールする

buildでパッケージをビルドしてインストールします。

```bash
python -m build
```

whlファイルを使ってインストールします。

```bash
python -m pip install ./dist/sample_package-0.1.0-py3-none-any.whl
```

パッケージがインストールされたことを確認します。

```bash
python -m pip list | grep sample
```

## パッケージをアンインストールする

作成したパッケージをアンインストールします。

```bash
python -m pip uninstall -y sample_package
```

## パッケージを解凍する

Pythonのパッケージは、tar.gzファイルなのでコマンドで解凍できます。解凍して中身を確認します。

```bash
tar xzf dist/sample_package-0.1.0.tar.gz
```

## 参考

- [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [Building and Publishing](https://packaging.python.org/en/latest/guides/section-build-and-publish/)
- [ビルド済み配布物を作成する](https://docs.python.org/ja/3.10/distutils/builtdist.html)
- [Package Discovery and Namespace Packages](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html)
