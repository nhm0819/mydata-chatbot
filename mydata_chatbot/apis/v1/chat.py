import logging
from asyncio import exceptions

from fastapi import APIRouter
from starlette.responses import PlainTextResponse, StreamingResponse
from starlette.types import Send
import json

from mydata_chatbot import agents
from mydata_chatbot.schemas.prompt import Prompt


router = APIRouter(prefix="/v1/chat/gpt")

logger = logging.getLogger(__name__)

llms = {
    "gpt": agents.gpt.build(),
    # "react": agents.react.build(),
}


@router.post("/{model_version}/invoke", response_class=PlainTextResponse)
async def invoke(model_version: str, p: Prompt) -> PlainTextResponse:
    agent = llms["gpt"]
    res = await agent.ainvoke(
        input={"input": p.user_query},
        config={
            "configurable": {"session_id": p.session_id, "gpt_version": model_version}
        },
    )
    return res["output"]


@router.post("/{model_version}/stream", response_class=StreamingResponse)
async def stream(model_version: str, p: Prompt) -> StreamingResponse:
    logger.error(f"Streaming response for [{model_version.upper()}]")
    logger.error(f"{p.session_id}: {p.user_query}]")
    agent = llms["gpt"]

    async def generate():
        # async for event in agent.astream(
        #     input={"input": p.user_query},
        #     config={"configurable": {"session_id": p.session_id, "gpt_version": model_version}},
        # ):
        async for event in agent.astream_events(
            input={"input": p.user_query},
            config={
                "configurable": {
                    "session_id": p.session_id,
                    "gpt_version": model_version,
                }
            },
            version="v1",
        ):
            kind = event["event"]
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    # Empty content in the context of OpenAI means
                    # that the model is asking for a tool to be invoked.
                    # So we only print non-empty content
                    yield content

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.post("/{model_version}/stream_events", response_class=StreamingResponse)
async def stream_events(model_version: str, p: Prompt) -> StreamingResponse:
    logger.error(f"Streaming response for [{model_version.upper()}]")
    logger.error(f"{p.session_id}: {p.user_query}]")
    agent = llms["gpt"]
    charset = "utf-8"

    async def generate():
        num_events = 0
        async for event in agent.astream_events(
            input={"input": p.user_query},
            config={
                "configurable": {
                    "session_id": p.session_id,
                    "gpt_version": model_version,
                }
            },
            version="v1",
        ):
            kind = event["event"]

            try:
                if kind == "on_chain_start":
                    if (
                        event["name"] == "agent"
                    ):  # matches `.with_config({"run_name": "Agent"})` in agent_executor
                        yield "\n"
                        yield (
                            f"Starting agent: {event['name']} "
                            f"with input: {event['data'].get('input')}"
                        )
                        yield "\n"
                elif kind == "on_chain_end":
                    if (
                        event["name"] == "agent"
                    ):  # matches `.with_config({"run_name": "Agent"})` in agent_executor
                        yield "\n"
                        yield (
                            f"Done agent: {event['name']} "
                            f"with output: {event['data'].get('output')['output']}"
                        )
                        yield "\n"
                if kind == "on_chat_model_stream":
                    content = event["data"]["chunk"].content
                    if content:
                        # Empty content in the context of OpenAI means
                        # that the model is asking for a tool to be invoked.
                        # So we only print non-empty content
                        yield content
                elif kind == "on_tool_start":
                    yield "\n"
                    yield (
                        f"Starting tool: {event['name']} "
                        f"with inputs: {event['data'].get('input')}"
                    )
                    yield "\n"
                elif kind == "on_tool_end":
                    yield "\n"
                    yield (
                        f"Done tool: {event['name']}\n"
                        # f"with output: {event['data'].get('output')}"
                    )
                    yield "\n"

            except Exception as exc:
                yield f"\n[Unhandled Error: {str(exc)}]"
                break

            finally:
                num_events += 1
                if num_events > 30:
                    # Truncate the output
                    yield "..."
                    break


    return StreamingResponse(generate(), media_type="text/event-stream")
