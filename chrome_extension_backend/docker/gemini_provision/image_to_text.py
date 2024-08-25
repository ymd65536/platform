import os

import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

project_id = os.environ.get("PROJECT_ID", "")


def get_text(gcs_file_path: str):
    res = _generate(Part.from_uri(gcs_file_path, mime_type="image/png"))
    return res


def _generate(image: Part):
    vertexai.init(project=project_id, location="asia-northeast1")
    responses = GenerativeModel("gemini-1.0-pro-vision-001").generate_content(
        [image, """画像に含まれているテキストを抜き出してください。"""],
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32,
        },
    )

    if responses.candidates:
        response_text = responses.candidates[0].text
    else:
        response_text = "No response"

    return response_text
