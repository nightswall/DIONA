FROM python:3.9
RUN apt-get update
RUN apt-get upgrade -y
RUN python -m pip install --upgrade pip

RUN pip install paho-mqtt

COPY ./app /app
WORKDIR /app