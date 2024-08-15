import os
import uuid
import logging
from datetime import datetime
from pytz import timezone
import asyncio
import streamlit as st
import httpx

tz = "Asia/Seoul"
tz_info = timezone(tz)

logging.Formatter.converter = lambda *args: datetime.now(tz=tz_info).timetuple()
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())

timeout = 30

if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())
    print(st.session_state["session_id"])

BACKEND_HOST = os.getenv("BACKEND_HOST", "http://127.0.0.1:8000")

st.set_page_config(page_title="챗봇", page_icon="🤖", layout="wide")

with st.sidebar:
    MODEL = st.selectbox("Choose a model", ["gpt"], key="model")
    STREAM_MODE = st.selectbox(
        "Choose a model", ["stream", "stream_events"], key="stream_mode"
    )

st.title(f"Finance Mydata Chatbot")
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.chat_message("assistant"):
    st.markdown("안녕하세요. 질문을 입력해주세요.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


async def streaming_response(user_query: str, session_id: str, **kwargs):
    url = f"{BACKEND_HOST}/v1/chat/{MODEL}/{STREAM_MODE}"
    if not url.startswith("http"):
        url = f"http://{url}"
    # url = f"{BACKEND_HOST}/v1/chat/{model}/stream_events"

    param = {
        "user_query": user_query,
        "session_id": session_id,
    }
    streamed_text = ""
    placeholder = st.empty()
    async with httpx.AsyncClient() as client:
        async with client.stream(
            method="POST", url=url, json=param, timeout=timeout
        ) as response:
            async for chunk in response.aiter_text():
                streamed_text += chunk
                placeholder.markdown(streamed_text)
                # st.write(chunk, unsafe_allow_html=True)

    return streamed_text


async def get_chat_answer(user_query):
    streamed_text = await streaming_response(
        user_query=user_query,
        session_id=st.session_state.session_id,
        model=MODEL,
    )

    st.session_state.messages.append({"role": "assistant", "content": streamed_text})


async def answer(user_query):
    await asyncio.gather(get_chat_answer(user_query))


async def main():
    if chat_input := st.chat_input("What's up?"):
        st.session_state.messages.append({"role": "user", "content": chat_input})
        with st.chat_message("user"):
            st.markdown(chat_input)

        with st.chat_message("assistant"):
            await answer(user_query=chat_input)


if __name__ == "__main__":
    asyncio.run(main())
