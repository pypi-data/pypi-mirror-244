import pytest

from bovine.crypto.types import CryptographicIdentifier

from . import create_app
from .config import Config
from .test_signature import public_key, valid_headers_for_key_id
from .test_public_key_cache import database  # noqa

from .model import RemoteIdentity


@pytest.fixture
def test_client(tmp_path):
    filename = str(tmp_path) + "/config.toml"
    config = Config.new(
        "http://localhost/actor_id",
        "acct:actor@domain",
        domain_blocks={"blocked.example"},
    )

    config.save(filename=filename)

    app = create_app(filename=filename)

    yield app.test_client()


async def test_get_index(test_client):
    response = await test_client.get("/")

    assert response.status_code == 200

    text = await response.get_data()

    assert "cattle_grid" in text.decode("utf-8")


async def test_get_actor(test_client):
    response = await test_client.get("/actor_id")

    assert response.status_code == 200

    result = await response.get_json()

    assert result["preferredUsername"] == "actor"


async def test_webfinger(test_client):
    response = await test_client.get(
        "/.well-known/webfinger?resource=acct:actor@domain"
    )

    assert response.status_code == 200

    result = await response.get_json()

    assert result["subject"] == "acct:actor@domain"


async def test_get_auth(test_client):
    response = await test_client.get("/auth")

    assert response.status_code == 200


async def test_get_auth_invalid_signature(test_client):
    response = await test_client.get("/auth", headers={"Signature": "invalid"})

    assert response.status_code == 401


async def test_get_auth_invalid_signature_cannot_get_key(test_client):
    response = await test_client.get(
        "/auth",
        headers={
            "Signature": '''keyId="https://remote.example/actor#key",algorithm="rsa-sha256",headers="(request-target) host",signature="inv sfdsfalid=="''',
            "X-Original-Method": "GET",
            "X-Original-Host": "remote.example",
            "X-Original-Uri": "/path",
            "Date": "today",
        },
    )

    assert response.status_code == 401


async def test_get_auth_invalid_signature_can_get_key(test_client, database):  # noqa
    controller = "https://remote.example/actor"
    key_id = f"{controller}#key"
    identifier = CryptographicIdentifier.from_pem(public_key, controller)
    public_key_multibase = identifier.as_tuple()[1]
    await RemoteIdentity.create(
        key_id=key_id,
        controller=controller,
        public_key=public_key_multibase,
    )

    response = await test_client.get(
        "/auth",
        headers=valid_headers_for_key_id(key_id),
    )

    assert response.status_code == 200

    assert response.headers["X-Cattle-Grid-Requester"] == controller


async def test_get_auth_invalid_signature_can_get_key_blocked(
    test_client, database  # noqa
):
    controller = "https://blocked.example/actor"
    key_id = f"{controller}#key"
    identifier = CryptographicIdentifier.from_pem(public_key, controller)
    public_key_multibase = identifier.as_tuple()[1]
    await RemoteIdentity.create(
        key_id=key_id,
        controller=controller,
        public_key=public_key_multibase,
    )

    response = await test_client.get(
        "/auth",
        headers=valid_headers_for_key_id(key_id),
    )

    assert response.status_code == 403
