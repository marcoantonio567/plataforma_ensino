from typing import Protocol


class CertificateRepository(Protocol):
    """Repository do aggregate root Certificado.

    IncidenteIntegridade e consultado para a politica de emissao, mas nao possui
    repository proprio porque pertence a fronteira da jornada/certificacao.
    """

    def get_or_create_for_enrollment(self, enrollment, *, expiration=None): ...
    def has_completed_project(self, enrollment, *, minimum_grade: float) -> bool: ...
    def has_severe_integrity_incident(self, enrollment) -> bool: ...
    def save(self, certificate, *, fields: list[str] | None = None) -> None: ...
