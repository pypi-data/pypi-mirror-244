import click
import tomllib
import tomli_w
import secrets
import logging
import os

from dataclasses import dataclass, asdict, field
from urllib.parse import urlparse
from urllib.request import urlopen
from functools import cached_property
from typing import Set


from bovine import BovineActor
from bovine.crypto import generate_rsa_public_private_key
from bovine.activitystreams import Actor
from bovine.utils import parse_fediverse_handle, webfinger_response_json


logger = logging.getLogger(__name__)


@dataclass
class Config:
    """Dataclass holding the configuration of cattle_grid

    :param actor_id: The URL the actor will be available at
    :param actor_acct_id: The acct id to use (reserves the username)
    :param db_url: url of the database used to store remote identities

    :param public_key: public key of cattle_grid actor
    :param private_key: private key of cattle_grid actor"""

    actor_id: str
    actor_acct_id: str
    db_url: str

    public_key: str
    private_key: str

    domain_blocks: Set[str] = field(default_factory=set)

    def is_blocked(self, uri):
        try:
            domain = urlparse(uri).netloc
            return domain in self.domain_blocks
        except Exception as e:
            logger.warning("Something went wrong with %s", repr(e))
            return True

    @staticmethod
    def new(actor_id, actor_acct_id, db_url=None, domain_blocks: Set[str] = set()):
        public_key, private_key = generate_rsa_public_private_key()

        if db_url is None:
            db_url = "sqlite://cattle_grid.sqlite"

        return Config(
            actor_id=actor_id,
            actor_acct_id=actor_acct_id,
            db_url=db_url,
            public_key=public_key,
            private_key=private_key,
            domain_blocks=domain_blocks,
        )

    @staticmethod
    def load(filename="cattle_grid.toml"):
        with open(filename, "rb") as fp:
            result = Config(**tomllib.load(fp))
            result.domain_blocks = set(result.domain_blocks)
            return result

    def save(self, filename="cattle_grid.toml"):
        with open(filename, "wb") as fp:
            data = asdict(self)
            data["domain_blocks"] = list(self.domain_blocks)
            tomli_w.dump(data, fp, multiline_strings=True)

    @property
    def actor_path(self):
        return urlparse(self.actor_id).path

    @cached_property
    def actor(self):
        username, _ = parse_fediverse_handle(self.actor_acct_id.removeprefix("acct:"))
        return Actor(
            id=self.actor_id,
            type="Service",
            public_key=self.public_key,
            preferred_username=username,
            public_key_name="mykey",
        ).build()

    @cached_property
    def webfinger(self):
        return webfinger_response_json(self.actor_acct_id, self.actor_id)

    @property
    def bovine_actor(self):
        actor = BovineActor(
            actor_id=self.actor_id,
            secret=self.private_key,
            public_key_url=self.actor_id + "#mykey",
        )
        return actor

    def add_blocks_from_url_or_file(self, url_or_file: str):
        """Adds the list of domains given by `url_or_file` to the
        blocklist. Assumes that each domain is on a new line.

        :param url_or_file: If it starts with `https://` is assumed to be an url
            otherwise as a file.
        """
        if url_or_file.startswith("https://"):
            with urlopen(url_or_file) as f:
                data = f.readlines()
        else:
            with open(url_or_file) as f:
                data = f.readlines()

        data = {
            x.decode("utf-8").removesuffix("\n")
            for x in data
            if x != b"canary.fedinuke.example.com\n"
        }

        self.domain_blocks = self.domain_blocks | data


@click.command
@click.option(
    "--actor_id",
    prompt="Actor id (e.g. http://cattle_grid/cattle_grid_actor)",
    help="Actor id with schema, e.g. http://cattle_grid/cattle_grid_actor",
)
@click.option(
    "--username",
    help="Used to in acct:username@domain. domain taken from actor id, leave blank for random",
)
@click.option("--db_url", help="database url by default sqlite file cattle_grid.sqlite")
@click.option(
    "--recreate",
    is_flag=True,
    default=False,
    help="Allows you to overwrite an existing cattle_grid.toml file",
)
def create_config(actor_id, username, db_url, recreate):
    if not recreate and os.path.exists("cattle_grid.toml"):
        click.echo("Configuration already exists")
        exit(1)

    if not username:
        username = secrets.token_urlsafe(12)
    if actor_id == "":
        actor_id = "http://cattle_grid/cattle_grid_actor"

    domain = urlparse(actor_id).netloc
    acct_uri = f"acct:{username}@{domain}"

    config = Config.new(actor_id, acct_uri, db_url=db_url)

    config.save()


if __name__ == "__main__":
    create_config()
