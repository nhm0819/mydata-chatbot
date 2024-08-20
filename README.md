# mydata-chatbot
- Mydata RAG with **Langchain** and **ChromaDB**
- Integration with **FastAPI**
- Fast shareable to use **Streamlit**
- Implementing multi-turn chatbot using sqlite (You can change to your db server)
- Use asynchronous functions for concurrency.

<br>

## Prerequisites
- Python 3.10 or later

<br>

## Installation
1. If you have poetry installed, run the following command:
```bash
poetry install
```

2. If not, run the following command:
```bash
pip install -r requirements.txt
```

<br>

## Getting Started
### Environments
- Create ".env" file in the same format as ".env.sample" file.
- Required
  - SQLITE_URL (or RDB_*)
  - OPENAI_API_KEY
``` yaml
# .env

ENV=dev  # if ENV=["dev", "stg"], verbose=True

### Database
SQLITE_URL=sqlite+aiosqlite:///sqlite3.db # Default
# RDB_USERNAME=NOT_APPLICABLE
# RDB_PASSWORD=NOT_APPLICABLE
# RDB_HOST=NOT_APPLICABLE
# RDB_DB_NAME=NOT_APPLICABLE


### Langsmith
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_PROJECT=hongmin
# LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
# LANGCHAIN_API_KEY=langchain_api_key

### OpenAI
OPENAI_API_KEY=openai_api_key # Required

### Tavily Search
# TAVILY_API_KEY=null

### Streamlit
# BACKEND_HOST=localhost:8000
```

<br>

### Preprocess (if you want to store more documents...)
if you do this, the documents in **fixtures** will be stored in chromadb **chroma/mydata_other_docs**.
1. add **.pdf** files in folder **"fixtures"**
2. insert **.pdf** data into **vector db(Chroma)** using python code below.
   1. python preprocess/pdf_to_md.py
   2. python preprocess/md_to_vectordb.py

<br>

### Run Backend Server
- run following command:
```bash
uvicorn mydata_chatbot.apps.v1:app # --env-file .env
```
<br>

### Try Streaming API
- The **backend server must be running**.
- run following code:
```python
import httpx
import asyncio

async def fetch_streaming_response():
    url = "http://127.0.0.1:8000/v1/chat/gpt/stream"
    ### if you want to know about tool usage history,
    # url = "http://127.0.0.1:8000/v1/chat/gpt/stream_events"
    user_query = "x-api-tran-id에 대해 알려주세요."
    params = {
        "user_query": user_query,
        "session_id": "foo",
    }
    async with httpx.AsyncClient() as client:
        async with client.stream("POST", url, json=params) as response:
            async for chunk in response.aiter_text():
                for character in chunk:
                    print(character, end="", flush=True)


asyncio.run(fetch_streaming_response())

```
<br>

### Use Chatbot with Streamlit
- The **backend server must be running**.
- run following command:
```bash
streamlit run strealit_async.py
```

<br>


## How to check agent progress? 
- You can use **Langsmith** (Free for 1 user; 5,000 free traces per month)
- You can test agent by running **mydata_chatbot/agents/gpt.py**.
   - Refer to the main function at the bottom 
- You can get results of agent tools in streaming by editing code. <br>Delete '#' in **mydata_chatbot/apis/v1/chat.py** in line 98. <br> and call **stream_events** func.
```python
elif kind == "on_tool_end":
    yield "\n"
    yield (
        f"Done tool: {event['name']}\n"
--->  # f"with output: {event['data'].get('output')}"
    )
    yield "\n"
```



<br>

## Run Locust(Stress Test)
- The **backend server must be running**.
- run following command:
```bash
locust -f tests/locustfile.py
```

<br>

## Pytest for agent streaming
- pytest
- set up the test env in "pytest.ini"
```bash
pytest
```

<br>

## Docker build
```dockerfile
# FastAPI (RAG backend)
docker build -t ${IMAGE_NAME}:{VERSION} -f dockers/fastapi.Dockerfile .
### mac OS
docker build --platform linux/amd64 -t ${IMAGE_NAME}:{VERSION} -f dockers/fastapi.Dockerfile .

# Streamlit
docker build [--platform linux/amd64] -t ${IMAGE_NAME}:{VERSION} -f dockers/streamlit.Dockerfile .
```
