from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from mydata_chatbot.crud.base import CRUDBase, ModelType
from mydata_chatbot.models.account import Account
from mydata_chatbot.schemas.account import AccountCreate, AccountUpdate


class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):
    async def get_by_uid(self, db: AsyncSession, uid: str) -> Optional[ModelType]:
        query = select(self.model).where(self.model.uid == uid)
        query_result = await db.execute(query)
        return query_result.scalar_one_or_none()


account = CRUDAccount(Account)
