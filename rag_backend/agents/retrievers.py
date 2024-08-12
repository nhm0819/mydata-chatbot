import re
from typing import List

from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


class FinanceMydataRetriever(BaseRetriever):

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:

        tool_name = "예시"
        text_0 = f"1. 아래 항목은 '{tool_name}' 을 이미 사용 한 결과입니다.\n"

        return [
            Document(page_content=text_0),
        ]


def format_by_newline(docs):
    return "\n\n".join([d.page_content for d in docs])
