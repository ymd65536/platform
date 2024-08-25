import os
import requests as requests
from google.cloud import storage


def download_obj(download_url):
    """画像をダウンロードする

    Args:
        download_url (str): 画像のURL

    Returns:
        bytes: 画像データ、ダウンロードに失敗した場合はNone
    """
    img_data = requests.get(
        download_url,
        stream=True,
    ).content

    if len(img_data) > 0:
        return img_data
    else:
        return None


def save_obj(download_url):
    image = download_obj(download_url)
    if image:
        bucket_name = os.environ.get("GCS_BUCKET_NAME", "")
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        year = download_url.split("/")[-3]
        month = download_url.split("/")[-2]
        img_name = download_url.split("/")[-1]
        filename = f"{year}_{month}_{img_name}"

        blob = bucket.blob(filename)
        blob.upload_from_string(image, content_type="image/png")
        return "Success"
    else:
        return "Failed to download image"
