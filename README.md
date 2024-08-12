# Prerequisites
- Python 3.11 or later

# Installation
1. If you have poetry installed, run the following command:
```bash
poetry update
```

2. If not, run the following command:
```bash
pip install -r requirements.txt
```

# Run Backend Server
- run following command:
```bash
gunicorn rag_backend.apps.v1:app -c gunicorn.conf.py
```

# Run Streamlit Server
- The **backend server must be running**.
- run following command:
```bash
streamlit run strealit_async.py
```

# Run Locust(Stress Test)
- run following command:
```bash
make locust
```

# Try Streaming API
- run following code:
```python
import httpx
import asyncio

async def fetch_streaming_response():
    url = "http://127.0.0.1:8000/v1/chat/gpt/stream"
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