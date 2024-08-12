from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from rag_backend.crud.base import CRUDBase, ModelType
from rag_backend.models.account import Account
from rag_backend.schemas.account import AccountCreate, AccountUpdate


class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):
    async def get_by_uid(
        self, db: AsyncSession, uid: str
    ) -> Optional[ModelType]:
        query = select(self.model).where(self.model.uid == uid)
        query_result = await db.execute(query)
        return query_result.scalar_one_or_none()


account = CRUDAccount(Account)
