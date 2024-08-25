from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hoge():
    return request.get_data()


app.run()
