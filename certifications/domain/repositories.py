from typing import Protocol


class CertificateRepository(Protocol):
    def save(self, certificate, *, fields: list[str]) -> None: ...
