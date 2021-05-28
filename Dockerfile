# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /home/app
COPY requirements.txt /home/app/
RUN pip install -r requirements.txt
COPY . /home/app/
