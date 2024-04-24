import os
from flask import Flask, request
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)


@app.route("/")
def hello_world():
    req_params = request.args
    env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
    template = env.get_template('./template/template.html')
    params = {
        'name': req_params.get('name', 'World'),
        'result': req_params.get('result', 'Hello')
    }
    return template.render(params)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))