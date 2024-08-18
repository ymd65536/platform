# learn_flask

Flask、ナニモワカラナイ

## リクストデータを受信する

```py
from flask import Flask, request

app = Flask(__name__)
@app.route("/", methods=["POST"])
def rt_recv():
    get_json = request.get_json() # 本記事ではこの行のみ記述
    # get_json['test']
    # 単に表示させる
    # print(request.headers)

    # 辞書型で取得する
    # dict(request.headers)
  return get_json

app.run(host="0.0.0.0", port=8080, debug=True)
```

## jsonでcurl

`Content-type`が　`application/json`の場合

```bash
curl -X POST -H "Content-type: application/json"  -d '{"a":1}'  http://127.0.0.1:5000/
```

`Content-type`なし。

```bash
 curl -X POST -d '{"a":1}'  http://127.0.0.1:5000/
```

## あとで読みたい

[とほほのFlask入門](https://www.tohoho-web.com/ex/flask.html)
