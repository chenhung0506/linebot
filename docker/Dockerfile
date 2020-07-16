# FROM python:3.7-alpine
FROM chenhung0506/python-with-chrome:latest
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
# RUN mkdir -p /usr/local/bin
# ADD ./module/linux_chromedriver/chromedriver /usr/local/bin
# RUN apk add chromium chromium-chromedriver
# ARG testArg=$(pwd)
# RUN echo "testArg: $testArg"
# RUN apk add bash
# RUN pip install -r /usr/src/app/requirements.txt
ADD dev.env /usr/src/app
ADD ./module /usr/src/app
RUN ls /usr/src/app
CMD ["python", "server.py"]
# ENTRYPOINT [ "/code/test.py" ]