FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apt-get update && apt-get install -y gcc python3-dev musl-dev libpq-dev python3-pip postgresql-client

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ../../PycharmProjects/Web-scraper /app

RUN mkdir /dumps && chmod -R 777 /dumps
