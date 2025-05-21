# syntax=docker/dockerfile:1

FROM python:3.13-slim-bookworm
SHELL ["/bin/bash", "-c"]

RUN mkdir wd
WORKDIR wd

COPY . .

ARG TARGETPLATFORM

COPY requirements.txt .
RUN pip3 install -r requirements.txt

CMD [ "gunicorn", "--workers=8", "--threads=4", "-b 0.0.0.0:80", "app:server"]
