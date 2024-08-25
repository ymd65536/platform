# Chrome拡張機能のバックエンドを作る

## プロジェクトIDの取得

```bash
export PROJECT_ID=`gcloud config list --format 'value(core.project)'` && echo $PROJECT_ID
```

## Google Cloud認証

```bash
gcloud auth login
gcloud config set project $PROJECT_ID
gcloud auth configure-docker asia-northeast1-docker.pkg.dev
```

## ビルド

```bash
docker build . -t $image_name --platform linux/amd64
docker tag $image_name asia-northeast1-docker.pkg.dev/$PROJECT_ID_id/$image_name/$image_name
```

イメージを削除します。

```bash
docker rmi asia-northeast1-docker.pkg.dev/$PROJECT_ID_id/$image_name/$image_name && docker rmi $image_name
```

## リポジトリの作成

```bash
image_name=extension-backend
gcloud artifacts repositories create $image_name --location=asia-northeast1 --repository-format=docker --project=$PROJECT_ID_id
```

## イメージをリポジトリにプッシュ

```bash
docker push asia-northeast1-docker.pkg.dev/$PROJECT_ID_id/$image_name/$image_name":latest"
```
