# syntax=docker/dockerfile:1
FROM python:3.9-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /home/app
COPY requirements.txt /home/app/
RUN pip install -r requirements.txt
RUN useradd --home-dir /home/app --shell /sbin/nologin app
USER app
COPY . /home/app/
