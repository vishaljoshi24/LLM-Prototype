# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster
LABEL VERSION=1.0

RUN apt-get update && apt-get -y install cmake protobuf-compiler g++

WORKDIR /DnDChatbot

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
ENV FLASK_APP=llama-cpp-qna.py
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
