from langchain_community.chat_message_histories.sql import SQLChatMessageHistory
from langchain_core.messages import BaseMessage
from typing import List
from sqlalchemy import Column, Integer, Text, delete, select


class SQLChatMessageSummaryHistory(SQLChatMessageHistory):

    async def aget_messages(self) -> List[BaseMessage]:
        """Retrieve all messages from db"""
        await self._acreate_table_if_not_exists()
        async with self._make_async_session() as session:
            stmt = (
                select(self.sql_model_class)
                .where(
                    getattr(self.sql_model_class, self.session_id_field_name)
                    == self.session_id
                )
                .order_by(self.sql_model_class.id.asc())
            )
            result = await session.execute(stmt)
            messages = []
            for record in result.scalars():
                messages.append(self.converter.from_sql_model(record))

            return messages[-5:]
