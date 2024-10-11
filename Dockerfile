FROM python:3.12.3-slim

WORKDIR /app

COPY . /app

COPY requirements.txt /app

RUN pip install -r requirements.txt