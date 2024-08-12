from uuid import UUID

import pytest
from httpx import AsyncClient
from pytest_mock import MockerFixture

from rag_backend.models import Account


@pytest.mark.asyncio
async def test_example_1(client: AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code == 200
    assert response.text == "Hello, World!"
