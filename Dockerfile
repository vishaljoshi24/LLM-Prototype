# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster
LABEL VERSION=1.0

RUN apt-get update && apt-get -y install cmake protobuf-compiler g++

WORKDIR /DnDChatbot

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "LLM_Prototype.py", "--server.port=8501", "--server.address=0.0.0.0"]
