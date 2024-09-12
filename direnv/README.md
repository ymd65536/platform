# direnvを使う

## direnvのインストール

```bash
brew install go
```

```bash
git clone https://github.com/direnv/direnv
cd direnv
```

```bash
sudo make install
```

実行結果

```text
install -d /usr/local/bin
install direnv /usr/local/bin
install -d /usr/local/share/man/man1
cp -R man/*.1 /usr/local/share/man/man1
install -d /usr/local/share/fish/vendor_conf.d
echo "/usr/local/bin/direnv hook fish | source" > /usr/local/share/fish/vendor_conf.d/direnv.fish
```

## direnvの設定

プロファイルに設定を追記します。

```bash
echo 'eval "$(direnv hook bash)"' >> ~/.bash_profile
```

ターミナルを再起動するかもしくは以下のコマンドを実行します。

```bash
source ~/.bash_profile
```

規定のエディタを設定します。

```bash
export EDITOR=vi
```

`.envrc`を作成します。

```bash
direnv edit .
```

以下の内容を記述します。

```bash
# ここで設定したTESTはカレントディレクトリ配下のみ有効にできる
export TEST=test

# 上位フォルダで設定した環境変数の削除（unset)もできる
unset ABC
```

## 参考

- [direnv](https://github.com/direnv/direnv/blob/master/docs/hook.md)
