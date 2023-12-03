from unittest.mock import AsyncMock
from bovine.crypto.types import CryptographicIdentifier

from .signature import SignatureChecker


public_key = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA15vhFdK272bbGDzLtypo
4Nn8mNFY3YSLnrAOX4zZKkNmWmgypgDP8qXjNiVsBf8f+Yk3tHDs58LMf8QDSP09
A+zrlWBHN1rLELn0JBgqT9xj8WSobDIjOjFBAy4FKUko7k/IsYwTl/Vnx1tykhPR
1UzbaNqN1yQSy0zGbIce/Xhqlzm6u+twyuHVCtbGPcPh7for5o0avKdMwhAXpWMr
Noc9L2L/9h3UgoePgAvCE6HTPXEBPesUBlTULcRxMXIZJ7P6eMkb2pGUCDlVF4EN
vcxZAG8Pb7HQp9nzVwK4OXZclKsH1YK0G8oBGTxnroBtq7cJbrJvqNMNOO5Yg3cu
6QIDAQAB
-----END PUBLIC KEY-----
"""


def valid_headers_for_key_id(key_id):
    return {
        "date": "Wed, 15 Mar 2023 17:28:15 GMT",
        "X-Original-Host": "myhost.example",
        "X-Original-Uri": "/path/to/resource",
        "X-Original-Method": "get",
        "signature": f'''keyId="{key_id}",algorithm="rsa-sha256",headers="(request-target) host date",signature="hUW2jMUkhiKTmAoqgq7CDz0l4nYiulbVNZflKu0Rxs34FyBs0zkBKLZLUnR35ptOvsZA7hyFOZbmK9VTw2VnoCvUYDPUb5VyO3MRpLv0pfXNExQEWuBMEcdvXTo30A0WIDSL95u7a6sQREjKKHD5+edW85WhhkqhPMtGpHe95cMItIBv6K5gACrsOYf8TyhtYqBxz8Et0iwoHnMzMCAHN4C+0nsGjqIfxlSqUSMrptjjov3EBEnVii9SEaWCH8AUE9kfh3FeZkT+v9eIDZdhj4+opnJlb9q2+7m/7YH0lxaXmqro0fhRFTd832wY/81LULix/pWTOmuJthpUF9w6jw=="''',
    }


async def test_signature_checker():
    retriever = AsyncMock(
        return_value=CryptographicIdentifier.from_pem(public_key, "owner")
    )
    checker = SignatureChecker(retriever)

    key_id = "https://remote.example/actor#key"
    result = await checker.verify_signature(valid_headers_for_key_id(key_id))

    assert result == "owner"


async def test_signature_checker_no_public_key():
    retriever = AsyncMock(return_value=None)
    checker = SignatureChecker(retriever)

    key_id = "https://remote.example/actor#key"
    result = await checker.verify_signature(valid_headers_for_key_id(key_id))

    assert result is None
