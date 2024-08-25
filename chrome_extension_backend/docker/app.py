import os
import rq_save_obj.gcs as gcs
import gemini_provision.image_to_text as image_to_text

from flask import Flask, request
from jinja2 import Environment, FileSystemLoader

wp_url = "url"

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World"


@app.route("/img", methods=["GET"])
def get_img_name():
    req = request.args
    year = req.get("year")
    month = req.get("month")
    img_name = req.get("img_name")
    request_url = f"{wp_url}/{year}/{month}/{img_name}"

    res = gcs.save_obj(request_url)
    return res


@app.route("/img/provision", methods=["GET"])
def gemini_pro_vision():
    req = request.args

    year = req.get("year")
    month = req.get("month")
    img_name = req.get("img_name")

    bucket_name = os.environ.get("GCS_BUCKET_NAME", "")
    gcs_file_path = f"gs://{bucket_name}/{year}_{month}_{img_name}"

    image_text = image_to_text.get_text(gcs_file_path)

    env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
    template = env.get_template('./template/template.html')
    params = {
        'scan_image': f"{wp_url}/{year}/{month}/{img_name}",
        'result': image_text
    }
    return template.render(params)


@app.route("/callback", methods=['POST'])
def callback():
    return "post callback!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))