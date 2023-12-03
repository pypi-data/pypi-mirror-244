import logging

from dataclasses import dataclass
from typing import Awaitable, Callable

from bovine.crypto.http_signature import HttpSignature
from bovine.crypto.signature import parse_signature_header
from bovine.crypto.types import CryptographicIdentifier

logger = logging.getLogger(__name__)


@dataclass
class SignatureChecker:
    key_retriever: Callable[str, Awaitable[CryptographicIdentifier | None]]

    async def verify_signature(self, headers) -> str | None:
        try:
            http_signature = HttpSignature()
            parsed_signature = parse_signature_header(headers["signature"])
            signature_fields = parsed_signature.fields

            for field in signature_fields:
                if field == "(request-target)":
                    method = headers.get("X-Original-Method").lower()
                    path = headers.get("X-Original-Uri")
                    http_signature.with_field(field, f"{method} {path}")
                elif field == "host":
                    http_signature.with_field(field, headers["X-Original-Host"])
                else:
                    http_signature.with_field(field, headers[field])

            identifier = await self.key_retriever(parsed_signature.key_id)

            if identifier is None:
                return None

            if http_signature.verify_with_identity(
                identifier, parsed_signature.signature
            ):
                return identifier.controller
        except Exception as e:
            logger.exception(e)
            logger.warning(headers)

        return None
