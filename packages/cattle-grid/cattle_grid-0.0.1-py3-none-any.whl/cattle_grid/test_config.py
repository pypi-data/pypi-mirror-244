import pytest
from bovine import BovineActor

from .config import Config


def test_new_config(tmp_path):
    filename = str(tmp_path) + "/config.toml"

    config = Config.new("actor_id", "acct:actor")

    assert isinstance(config, Config)

    assert config.public_key.startswith("-----BEGIN PUBLIC KEY-----")
    assert config.private_key.startswith("-----BEGIN PRIVATE KEY-----")

    config.save(filename)

    loaded = Config.load(filename)

    assert loaded.public_key == config.public_key
    assert isinstance(loaded.domain_blocks, set)


def test_actor_path():
    config = Config.new("http://cattle_grid/actor_id", "acct:actor")

    assert config.actor_path == "/actor_id"


def test_actor_get_actor():
    config = Config.new("http://cattle_grid/actor_id", "acct:actor@domain")

    actor = config.actor

    assert actor["type"] == "Service"
    assert actor["preferredUsername"] == "actor"


def test_bovine_actor():
    config = Config.new("http://cattle_grid/actor_id", "acct:actor@domain")

    assert isinstance(config.bovine_actor, BovineActor)


def test_webfinger():
    config = Config.new("http://cattle_grid/actor_id", "acct:actor@domain")

    webfinger = config.webfinger
    assert webfinger["subject"] == "acct:actor@domain"


def test_is_blocked():
    config = Config.new(
        "http://cattle_grid/actor_id",
        "acct:actor@domain",
        domain_blocks={"bad.example"},
    )

    assert not config.is_blocked("https://good.example/actor_uri")

    assert config.is_blocked("https://bad.example/actor/bad")


@pytest.mark.skip("Makes web request")
def test_add_blocks_from_url():
    config = Config.new(
        "http://cattle_grid/actor_id",
        "acct:actor@domain",
    )
    config.add_blocks_from_url_or_file("https://seirdy.one/pb/FediNuke.txt")

    assert config.is_blocked("https://poa.st/actor/bad")
