import json
import logging
from typing import Optional, Type
from langchain.tools.retriever import create_retriever_tool

from langchain.callbacks.manager import AsyncCallbackManagerForToolRun
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

# from rag_backend.database.chroma import (
#     disease_name_chroma,
# )

logger = logging.getLogger(__name__)


class SearchInsuranceRequirementsInput(BaseModel):
    disease_name: str = Field(description="보험 가입 때 등록 할 질병 명.")


class SearchInsuranceRequirementsTool(BaseTool):
    name: str = "search_insurance_requirements_tool"
    description: str = "보험 가입 시 필요한 서류를 조회 합니다."
    args_schema: Type[BaseModel] = SearchInsuranceRequirementsInput

    def _run(
        self,
        disease_name: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        documents = insurance_requirements_chroma.similarity_search(disease_name, k=3)
        metadata = [x.metadata for x in documents]
        return json.dumps(metadata, ensure_ascii=False, indent=2)

    async def _arun(
        self,
        disease_name: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        return self._run(disease_name)


class SearchDiseaseInput(BaseModel):
    query: str = Field(
        description=(
            "질병 이름 혹은 질병 증상등을 입력 합니다. "
            "'두통', '머리가 아파요' 혹은 '머리아픔' 같은 방식으로 입력 가능합니다."
        )
    )
    k: int = Field(
        description="검색 할 개수를 지정합니다. 기본값은 5 입니다.", default=5
    )


class SearchInsuranceInput(BaseModel):
    query: str = Field(
        description="질병 이름 혹은 질병 증상등을 바탕으로 입력합니다. Ex) '암 보험', '해약환급금이 없는 무배당 암보험'"
    )


class SearchInsuranceTool(BaseTool):
    name: str = "search_insurance_tool"
    description: str = (
        "특약 종류, 보험 종류, 보험 코드, 보험금 및 보상금 정보를 얻을 수 있는 데이터베이스를 조회합니다. "
        "유저가 특약이나 보험 종류 및 가입금액에 대해서 물을때 유용합니다."
    )
    args_schema: Type[BaseModel] = SearchInsuranceInput

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        insurance_docs = insurance_chroma.similarity_search(query, k=5)
        insurance_metas = [x.metadata for x in insurance_docs]
        if "여성" in query or "여자" in query:
            insurance_metas = [x for x in insurance_metas if x["성별"] == "여성"]
        dumps_1 = json.dumps(insurance_metas, ensure_ascii=False, indent=2)

        limit_docs = coverage_limit_chroma.similarity_search(query, k=5)
        limit_metas = [x.metadata for x in limit_docs]
        dumps_2 = json.dumps(limit_metas, ensure_ascii=False, indent=2)

        # formatting
        result = dumps_1 + "\n\n" + dumps_2
        result += "\n\n\n"
        result += "[경고]: 보험 상품 유형 검색시, 사용자가 기본형, 해약환급금에 대해 선택하지 않았을 경우, 두개 다 보여 주시오."
        return result

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        return self._run(query)


class GetInsuranceEnrollmentCriteriaInput(BaseModel):
    disease_name: str = Field(description="환자가 앓고 있는 질병에 대한 질병 이름")
    collateral_name: str = Field(
        description="보험에 추가 할 담보명 example) 암, 질병입원, 15대입원수술"
    )


class GetInsuranceEnrollmentCriteriaTool(BaseTool):
    name: str = "get_insurance_enrollment_criteria_tool"
    description: str = (
        "보험이나 특약에 가입하고 싶을 때 어떤 조건을 충족해야 하는지 조회합니다. "
        "질병이 있는 환자가 보험이나 특약을 추가하고 싶은 경우에만 가능합니다. "
        "환자의 질병명과 담보명을 입력하면 가입 가능 여부를 알려줍니다."
    )
    args_schema: Type[BaseModel] = GetInsuranceEnrollmentCriteriaInput

    def _run(
        self,
        disease_name: str,
        collateral_name: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:

        disease_name = self.make_sure_disease_name(disease_name)
        collateral_name = self.make_sure_collateral_name(collateral_name)

        allowed_diseases = [
            "만성신우신염",
            "코로나19 합병증",
            "심근경색증",
            "폐렴, 기관지염",
        ]
        if disease_name not in allowed_diseases:
            return (
                "현재 지원되지 않는 질병 입니다."
                + "\n"
                + "지원 되는 질병명: "
                + ", ".join(allowed_diseases)
            )

        if run_manager:
            run_manager.on_text(
                f"```\n\n\n질병명: {disease_name}\n담보명: {collateral_name}\n\n\n```"
            )

        criteria_condition = self.get_criteria_condition(disease_name)
        criteria_description = self.get_criteria_from_matrix(
            disease_name, collateral_name
        )

        logger.info(f"chosen collateral name: {collateral_name}")
        logger.info(f"chosen criteria: {criteria_description}")

        answer = f"""
{criteria_description}

위 기준을 파악하기 위해서 물어봐야 할 필수 질문들:

{criteria_condition}

이미 답변이 된 부분은 답변을 같이 표기하시오.
"""
        return answer

    async def _arun(
        self,
        disease_name: str,
        collateral_name: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        return self._run(disease_name, collateral_name)

    def make_sure_collateral_name(self, collateral: str) -> str:
        """가장 가까운 담보명으로 변환합니다."""
        collateral_names = collateral_name_chroma.similarity_search(collateral, k=1)
        return collateral_names[0].page_content

    def make_sure_disease_name(self, collateral: str) -> str:
        """가장 가까운 질병명으로 변환합니다."""
        disease_names = disease_name_chroma.similarity_search(collateral, k=1)
        return disease_names[0].page_content
