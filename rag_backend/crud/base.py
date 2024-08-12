from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, text
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession

from rag_backend.models import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == id)
        query_result = await db.execute(query)
        return query_result.scalar_one_or_none()

    async def get_multi(
        self,
        *,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        query: str | None = None,
    ) -> List[ModelType]:
        if query is None:
            query = select(self.model).offset(skip).order_by(self.model.id)
        elif isinstance(query, str):
            query = text(query)

        if limit is not None:
            query = query.limit(limit)

        query_result = await db.execute(query)

        return query_result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore

        try:
            db.add(db_obj)
            await db.commit()
        except exc.IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=409,
                detail="Resource already exists",
            )
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(
                exclude_unset=True
            )  # This tells Pydantic to not include the values that were not sent
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> ModelType:
        query_result = await db.execute(select(self.model).where(self.model.id == id))
        obj = query_result.scalar_one()
        await db.delete(obj)
        await db.commit()
        return obj
