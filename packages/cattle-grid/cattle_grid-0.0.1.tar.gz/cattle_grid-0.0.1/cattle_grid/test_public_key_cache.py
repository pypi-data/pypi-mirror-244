import pytest
from unittest.mock import AsyncMock
from tortoise import Tortoise
from bovine.activitystreams import Actor

from .public_key_cache import PublicKeyCache
from .test_signature import public_key


@pytest.fixture
async def database():
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["cattle_grid.model"]},
    )
    await Tortoise.generate_schemas()
    yield "database"
    await Tortoise.close_connections()


async def test_public_key_cache():
    actor = Actor("actor_id", public_key=public_key, public_key_name="key").build()
    bovine_actor = AsyncMock()
    bovine_actor.get.return_value = actor

    cache = PublicKeyCache(bovine_actor)

    result = await cache.public_key_owner("some_id")
    assert result.controller == "actor_id"

    bovine_actor.get.assert_awaited_once()


async def test_cached_public_key(database):
    actor = Actor("actor_id", public_key=public_key, public_key_name="key").build()
    bovine_actor = AsyncMock()
    bovine_actor.get.return_value = actor

    cache = PublicKeyCache(bovine_actor)

    result = await cache.from_cache("some_id")
    assert result.controller == "actor_id"

    result = await cache.from_cache("some_id")
    assert result.controller == "actor_id"

    bovine_actor.get.assert_awaited_once()


async def test_public_key_cache_no_key_result(database):
    actor = Actor("actor_id").build()
    bovine_actor = AsyncMock()
    bovine_actor.get.return_value = actor

    cache = PublicKeyCache(bovine_actor)

    result = await cache.from_cache("some_id")
    assert result is None

    bovine_actor.get.assert_awaited_once()
