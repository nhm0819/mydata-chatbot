import asyncio

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_gpt_stream(client: AsyncClient) -> None:
    response = await client.post(
        "/v1/agent/gpt/stream",
        json={
            "message": "hello",
            "session_id": "mock-session-id",
        },
    )
    assert response.status_code == 200
