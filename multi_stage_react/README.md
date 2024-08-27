# React コンテナをマルチステージビルドで作成する

## 手順

```bash
cd src
```

```bash
docker build . -t test_react
```

```bash
docker run -d -p 80:80 --name run_react test_react
```

```bash
docker ps
```

```bash
docker exec -it run_react sh
```
