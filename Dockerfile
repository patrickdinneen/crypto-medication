FROM python:3.7-alpine
MAINTAINER patrick.dinneen@gmail.com

RUN mkdir /app
COPY . /app/
COPY requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /app

ENTRYPOINT ["python", "main.py"]