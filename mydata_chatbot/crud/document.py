from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from mydata_chatbot.crud.base import CRUDBase, ModelType
from mydata_chatbot.models.document import Document
from mydata_chatbot.schemas.document import DocumentCreate, DocumentUpdate


class CRUDDocument(CRUDBase[Document, DocumentCreate, DocumentUpdate]):
    async def get_by_filename(self, db: AsyncSession, filename: str) -> Optional[ModelType]:
        query = select(self.model).where(self.model.filename == filename)
        query_result = await db.execute(query)
        return query_result.all()


document = CRUDDocument(Document)
