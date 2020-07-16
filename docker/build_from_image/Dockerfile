FROM python:3.7-alpine
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
RUN apk add bash
RUN apk add chromium chromium-chromedriver
ADD requirements.txt /usr/src/app
RUN pip install -r /usr/src/app/requirements.txt

