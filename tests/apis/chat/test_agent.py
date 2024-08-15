import asyncio

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_gpt_stream(client: AsyncClient) -> None:
    response = await client.post(
        "/v1/chat/gpt/stream",
        json={
            "user_query": "x-tran-api-id에 대해 알려줘",
            "session_id": "mock-session-id",
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_gpt_stream_events(client: AsyncClient) -> None:
    response = await client.post(
        "/v1/chat/gpt/stream_events",
        json={
            "user_query": "x-tran-api-id에 대해 알려줘",
            "session_id": "mock-session-id",
        },
    )
    assert response.status_code == 200
