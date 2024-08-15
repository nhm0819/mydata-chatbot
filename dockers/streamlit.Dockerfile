FROM python:3.11-slim-buster

RUN apt-get update && apt-get install -y git

#COPY requirements.txt /opt/rag-backend/requirements.txt
#RUN pip install -r /opt/rag-backend/requirements.txt --no-cache-dir
RUN pip install streamlit
RUN pip install watchdog
RUN pip install httpx


COPY ../.. /opt/rag-backend
WORKDIR /opt/rag-backend

RUN ls -l /opt/rag-backend

EXPOSE 8501

CMD ["sh", "-c", "streamlit run streamlit_async.py"]
