# php-docker

This is a simple PHP Docker container that can be used to run PHP applications.

## Usage

To use this container, you can run the following command:

```bash
cd src/simple
docker run -it --rm --name my-running-script -v "$PWD":/usr/src/myapp -w /usr/src/myapp php:8.2-cli php script_local.php
```

## Building the image

```bash
docker build -t my-php-app .
docker run -it --rm --name my-running-app my-php-app
docker rmi my-php-app
```

## docker compose

```bash
docker compose up -d
docker-compose exec my-php-app composer --version
docker-compose exec my-php-app composer update
docker-compose exec my-php-app composer install
docker compose down
```

## compose set

```bash
composer require grpc/grpc
composer require google/protobuf
composer require momentohq/client-sdk-php
```