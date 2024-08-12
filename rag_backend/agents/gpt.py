import asyncio
from operator import itemgetter
from typing import Sequence
import os

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.tools import BaseTool
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain_openai import ChatOpenAI
from langchain.tools.retriever import create_retriever_tool

from langchain_community.chat_message_histories.sql import SQLChatMessageHistory
from langchain_community.tools.tavily_search import TavilySearchResults

from rag_backend.database import engine
from rag_backend.agents.prompts import mydata_prompt
from rag_backend.database.chroma import (
    mydata_api_docs_chroma,
    mydata_guideline_docs_chroma,
    mydata_other_docs_chroma,
)
from rag_backend.agents.retrievers import format_by_newline

from rag_backend.configs import settings


def build():
    # llm
    llm = ChatOpenAI(model=settings.openai_model, temperature=1e-10, streaming=True)

    # tools
    tools = []

    if os.getenv("TAVILY_API_KEY"):
        tools.append(
            TavilySearchResults(
                max_results=5,
                search_depth="advanced",
                include_answer=True,
                include_raw_content=True,
                include_images=True,
                # include_domains=[...],
                # exclude_domains=[...],
                # name="...",            # overwrite default tool name
                # description="...",     # overwrite default tool description
                # args_schema=...,       # overwrite default args_schema: BaseModel
            )
        )

    tools.append(
        create_retriever_tool(
            mydata_guideline_docs_chroma.as_retriever(
                search_type="mmr",
                search_kwargs={
                    "k": 5,
                    "fetch_k": 20,
                },
            ),
            name="mydata_guideline_docs_search",
            description="데이터 사용 정책 및 규정에 대한 질문이 들어오면 이 도구를 사용합니다.",
        )
    )

    tools.append(
        create_retriever_tool(
            mydata_api_docs_chroma.as_retriever(
                search_type="mmr",
                search_kwargs={
                    "k": 5,
                    "fetch_k": 20,
                },
            ),
            name="mydata_api_docs_search",
            description="API에 대한 상세한 질문이 들어오면 이 도구를 사용해야 합니다.",
        )
    )

    # tools.append(
    #     create_retriever_tool(
    #         mydata_other_docs_chroma.as_retriever(
    #             search_type="mmr",
    #             search_kwargs={
    #                 'k': 5,
    #                 'fetch_k': 20,
    #             }
    #         ),
    #         name="mydata_other_docs_search",
    #         description="질문에 대해 사용할 도구가 없다면 이 도구를 사용해야 합니다.",
    #     )
    # )

    agent = create_openai_tools_agent(llm, tools, mydata_prompt)

    if os.getenv("ENV") in ["dev", "stg"]:
        verbose = True
    else:
        verbose = False
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=verbose)

    return RunnableWithMessageHistory(
        agent_executor,
        get_session_history=lambda session_id: SQLChatMessageHistory(
            session_id=session_id, connection=engine
        ),
        input_messages_key="input",
        output_messages_key="output",
        history_messages_key="chat_history",
    )


async def main():
    from langchain.globals import set_verbose
    set_verbose(True)

    agent = build()
    while True:
        message = input("Enter a message: ")
        async for event in agent.astream(
            input={"input": message},
            config={"configurable": {"session_id": "foo"}},
        ):
            print(event)

        """if you want to see stream_event..."""
        # async def generate():
        #     async for event in agent.astream_events(
        #         input={"input": message},
        #         config={"configurable": {"session_id": "foo"}},
        #         version="v1",
        #     ):
        #         kind = event["event"]
        #         if kind == "on_chain_start":
        #             if (
        #                     event["name"] == "agent"
        #             ):  # matches `.with_config({"run_name": "Agent"})` in agent_executor
        #                 yield "\n"
        #                 yield (
        #                     f"Starting agent: {event['name']} "
        #                     f"with input: {event['data'].get('input')}"
        #                 )
        #                 yield "\n"
        #         elif kind == "on_chain_end":
        #             if (
        #                     event["name"] == "agent"
        #             ):  # matches `.with_config({"run_name": "Agent"})` in agent_executor
        #                 yield "\n"
        #                 yield (
        #                     f"Done agent: {event['name']} "
        #                     f"with output: {event['data'].get('output')['output']}"
        #                 )
        #                 yield "\n"
        #         if kind == "on_chat_model_stream":
        #             content = event["data"]["chunk"].content
        #             if content:
        #                 # Empty content in the context of OpenAI means
        #                 # that the model is asking for a tool to be invoked.
        #                 # So we only print non-empty content
        #                 yield content
        #         elif kind == "on_tool_start":
        #             yield "\n"
        #             yield (
        #                 f"Starting tool: {event['name']} "
        #                 f"with inputs: {event['data'].get('input')}"
        #             )
        #             yield "\n"
        #         elif kind == "on_tool_end":
        #             yield "\n"
        #             yield (
        #                 f"Done tool: {event['name']} "
        #                 f"with output:\n{event['data'].get('output')}"
        #             )
        #             yield "\n"
        #
        # async for chunk in generate():
        #     print(chunk, end="")


if __name__ == "__main__":
    asyncio.run(main())
