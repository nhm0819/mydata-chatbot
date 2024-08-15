# RAG-Backend
- RAG chatbot with Langchain and ChromaDB
- integration with FastAPI
- fast shareable to use Streamlit

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
SQLITE_URL=sqlite+aiosqlite:///sqlite3.db # Default
# RDB_USERNAME=NOT_APPLICABLE
# RDB_PASSWORD=NOT_APPLICABLE
# RDB_HOST=NOT_APPLICABLE
# RDB_DB_NAME=NOT_APPLICABLE

# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_PROJECT=hongmin
# LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
# LANGCHAIN_API_KEY=langchain_api_key

OPENAI_MODEL=gpt-3.5-turbo # put in openai model name
OPENAI_API_KEY=openai_api_key # Required

# TAVILY_API_KEY=null

# BACKEND_HOST=localhost:8000
```

### Preprocess
1. add .pdf files in folder "./fixtures/"
   - default 2 files in chroma db
     - chroma/mydata_api_docs
     - chroma/mydata_guideline_docs
2. insert into Vector Database(Chroma) to use below.
   1. python preprocess/pdf_to_md.py
   2. python preprocess/md_to_vectordb.py


### Run Backend Server
- run following command:
```bash
uvicorn rag_backend.apps.v1:app # --env-file .env
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


## Debug
1. You can use **Langsmith** (Free for 1 user; 5,000 free traces per month)
2. run rag_backend/agents/gpt.py
   1. refer to the **main** function at the bottom
3. You can get retriever result. get rid of '#' in **rag_backend/apis/v1/chat.py** in line 98.
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

## Agent Error Test
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
