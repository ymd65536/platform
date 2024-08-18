# Introduction

want to application develop by Flask

## SetUp

To build the environment necessary to create an application
Execute the following command.

```bash
pip install pipenv
pipenv --version
pipenv --python 3.8
pipenv shell
```

## What is Flask ?

Flask is a lightweight web application framework that can be written in Python.
Flask is called Micro Framework

Flask's Features

- You can create an application with a single file.

## Why use Flask?

## How to install

To install Flask, execute the following command.

```bash
pipenv install Flask
```

## How to execute

```bash
cd flask_blog_app
python server.py
```

## Run Dynamodb Local

```bash
java "-Djava.library.path=./DynamoDBLocal_lib" -jar DynamoDBLocal.jar -sharedDb
```

## test commands

```bash
$env:FLASK_ENV="development"
$env:FLASK_APP="hello.py"
flask run
```
