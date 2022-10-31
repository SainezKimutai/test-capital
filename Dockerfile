FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y install binutils libproj-dev gdal-bin

# Configs for mysqlclient
RUN apt-get -y install default-libmysqlclient-dev python3-dev build-essential default-mysql-client 

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app
