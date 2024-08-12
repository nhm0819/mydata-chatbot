from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import SystemMessagePromptTemplate

mydata_prompt = ChatPromptTemplate(
    input_variables=["agent_scratchpad", "chat_history", "input"],
    messages=[
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=[],
                template="당신은 금융 데이터 가이드라인을 안내합니다."
                "개인 신용정보를 사용하는 규칙에 대해 설명합니다.",
            )
        ),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["input"],
                template="{input}",
            )
        ),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ],
)
