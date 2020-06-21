from typing import Any

class PyCryptoVerifier:
    def __init__(self, pubkey: Any) -> None: ...
    def verify(self, message: Any, signature: Any): ...
    @staticmethod
    def from_string(key_pem: Any, is_x509_cert: Any): ...

class PyCryptoSigner:
    def __init__(self, pkey: Any) -> None: ...
    def sign(self, message: Any): ...
    @staticmethod
    def from_string(key: Any, password: str = ...): ...