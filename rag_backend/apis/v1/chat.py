import logging

from fastapi import APIRouter
from starlette.responses import PlainTextResponse, StreamingResponse

from rag_backend import agents
from rag_backend.schemas.prompt import Prompt


router = APIRouter(prefix="/v1/chat")

logger = logging.getLogger(__name__)

llms = {
    "gpt": agents.gpt.build(),
    # "react": agents.react.build(),
}


@router.post("/{model}/invoke", response_class=PlainTextResponse)
async def invoke(model: str, p: Prompt) -> PlainTextResponse:
    agent = llms[model]
    res = await agent.ainvoke(
        input={"input": p.user_query},
        config={"configurable": {"session_id": p.session_id}},
    )
    return res["output"]


@router.post("/{model}/stream", response_class=StreamingResponse)
async def stream(model: str, p: Prompt) -> StreamingResponse:
    logger.error(f"Streaming response for [{model.upper()}]")
    logger.error(f"{p.session_id}: {p.user_query}]")
    agent = llms[model]

    async def generate():
        async for event in agent.astream(
            input={"input": p.user_query},
            config={"configurable": {"session_id": p.session_id}},
        ):
            if "output" in event.keys():
                yield event["output"]

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.post("/{model}/stream_events", response_class=StreamingResponse)
async def stream_events(model: str, p: Prompt) -> StreamingResponse:
    logger.error(f"Streaming response for [{model.upper()}]")
    logger.error(f"{p.session_id}: {p.user_query}]")
    agent = llms[model]

    async def generate():
        async for event in agent.astream_events(
            input={"input": p.user_query},
            config={"configurable": {"session_id": p.session_id}},
            version="v1",
        ):
            kind = event["event"]
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

    return StreamingResponse(generate(), media_type="text/event-stream")
