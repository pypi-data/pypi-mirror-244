from dataclasses import dataclass
import logging

from bovine import BovineActor
from bovine.crypto.types import CryptographicIdentifier
from fediverse_pasture.server.utils import actor_object_to_public_key

from .model import RemoteIdentity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PublicKeyCache:
    bovine_actor: BovineActor

    async def public_key_owner(self, key_id: str) -> CryptographicIdentifier | None:
        try:
            result = await self.bovine_actor.get(key_id)
            public_key, owner = actor_object_to_public_key(result, key_id)
            return CryptographicIdentifier.from_pem(public_key, owner)
        except Exception as e:
            logger.info("Failed to fetch public key for %s with %s", key_id, repr(e))
            # logger.exception(e)
            return None

    async def from_cache(self, key_id: str) -> CryptographicIdentifier | None:
        identity = await RemoteIdentity.get_or_none(key_id=key_id)

        if identity is None:
            identifier = await self.public_key_owner(key_id)
            if identifier is None:
                return None
            try:
                controller, public_key = identifier.as_tuple()
                identity = await RemoteIdentity.create(
                    key_id=key_id, public_key=public_key, controller=controller
                )
                await identity.save()
            except Exception as e:
                logger.exception(e)
            return identifier

        return CryptographicIdentifier.from_tuple(
            identity.controller, identity.public_key
        )
