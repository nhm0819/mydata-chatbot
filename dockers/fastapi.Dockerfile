FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y git

COPY requirements.txt /opt/rag-backend/requirements.txt
#RUN pip install --upgrade pip

RUN pip install -r /opt/rag-backend/requirements.txt --no-cache-dir
RUN pip install pysqlite3-binary --no-cache-dir
#RUN pip install numexpr

COPY ../.. /opt/rag-backend
WORKDIR /opt/rag-backend

RUN ls -l /opt/rag-backend

#EXPOSE 8000

CMD uvicorn --host 0.0.0.0 --port 8000 mydata_chatbot.apps.v1:app
